"""
See https://www.w3.org/TR/webauthn/#api
"""
import re, json, copy, secrets, base64, struct, hashlib, textwrap

import cbor2

from .attestation import FIDOU2FAttestationStatement
from .cose import COSE
from .credentials import Credential

class AuthenticatorData:
    def __init__(self, auth_data):
        self.raw_auth_data = auth_data
        self.rp_id_hash, flags, self.signature_counter = struct.unpack(">32s1sI", auth_data[:37])
        flags = [bool(int(i)) for i in format(ord(flags), "08b")]
        (self.extension_data_included,
         self.attested_credential_data_included, _, _, _,
         self.user_verified, _,
         self.user_present) = flags
        self.credential = None
        if self.attested_credential_data_included:
            aaguid, credential_id_length = struct.unpack(">16sH", auth_data[37:55])
            credential_id = auth_data[55:55 + credential_id_length]
            cose_credential_public_key = auth_data[55 + credential_id_length:]
            self.credential = Credential(credential_id=credential_id, credential_public_key=cose_credential_public_key)

class RelyingPartyManager:
    registration_options = {
        "challenge": None,
        "rp": {
            "name": "akislyuk-czi-wa-test"
        },
        "user": {
            "id": None,
            "name": "akislyuk@chanzuckerberg.com",
            "displayName": "Andrey Kislyuk",
            "icon": "https://avatars1.githubusercontent.com/u/862013"
        },
        "pubKeyCredParams": [
            {
                "type": "public-key",
                "alg": COSE.ALGORITHMS.ES256
            }
        ],
        "timeout": 60000,  # 1 minute
        "excludeCredentials": [],  # No exclude list of PKCredDescriptors
        "attestation": "direct",
        "extensions": {"loc": True}  # Include location information in attestation
    }

    authentication_options = {
        "challenge": None,
        "timeout": 60000,  # 1 minute
        "allowCredentials": []
    }

    def __init__(self, credential_storage_backend):
        self.storage_backend = credential_storage_backend

    def get_registration_options(self, email):
        "Get challenge parameters that will be passed to the user agent's navigator.credentials.get() method"
        options = copy.deepcopy(self.registration_options)
        options["user"]["name"] = email
        options["user"]["id"] = base64.b64encode(email.encode()).decode()
        options["challenge"] = base64.b64encode(secrets.token_bytes(32)).decode()
        return options

    def get_authentication_options(self, email):
        credential = self.storage_backend.get_credential_by_email(email)
        options = copy.deepcopy(self.authentication_options)
        options["challenge"] = base64.b64encode(secrets.token_bytes(32)).decode()
        options["allowCredentials"] = [{"type": "public-key", "id": base64.b64encode(credential.id).decode()}]
        return options

    # https://www.w3.org/TR/webauthn/#registering-a-new-credential
    def register(self, client_data_json, attestation_object, email):
        "Store the credential public key and related metadata on the server using the associated storage backend"
        authenticator_attestation_response = cbor2.loads(attestation_object)
        email = email.decode()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise Exception("Invalid email address")
        client_data_hash = hashlib.sha256(client_data_json).digest()
        client_data = json.loads(client_data_json)
        assert client_data["type"] == "webauthn.create"
        # assert client_data["challenge"] is valid
        # Verify that the value of C.origin matches the Relying Party's origin.
        # Verify that the RP ID hash in authData is indeed the SHA-256 hash of the RP ID expected by the RP.
        authenticator_data = AuthenticatorData(authenticator_attestation_response["authData"])
        assert authenticator_data.user_present
        # If user verification is required for this registration, verify that the User Verified bit of the flags in authData is set.
        assert authenticator_attestation_response["fmt"] == "fido-u2f"
        att_stmt = FIDOU2FAttestationStatement(authenticator_attestation_response['attStmt'])
        attestation = att_stmt.validate(authenticator_data, rp_id_hash=authenticator_data.rp_id_hash, client_data_hash=client_data_hash)
        credential = attestation.credential
        # TODO: ascertain user identity here
        self.storage_backend.save_credential_for_user(email=email, credential=credential)
        return {"registered": True}

    # https://www.w3.org/TR/webauthn/#verifying-assertion
    def verify(self, authenticator_data, client_data_json, signature, user_handle, raw_id, email):
        "Ascertain the validity of credentials supplied by the client user agent via navigator.credentials.get()"
        email = email.decode()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise Exception("Invalid email address")
        client_data_hash = hashlib.sha256(client_data_json).digest()
        client_data = json.loads(client_data_json)
        assert client_data["type"] == "webauthn.get"
        # assert client_data["challenge"] is valid
        # Verify that the value of C.origin matches the Relying Party's origin.
        # Verify that the RP ID hash in authData is indeed the SHA-256 hash of the RP ID expected by the RP.
        authenticator_data = AuthenticatorData(authenticator_data)
        assert authenticator_data.user_present
        credential = self.storage_backend.get_credential_by_email(email)
        credential.verify(signature, authenticator_data.raw_auth_data + client_data_hash)
        # signature counter check
        return {"verified": True}

from .credentials import Credential

class CredentialStorageBackend:
    def __init__(self):
        raise NotImplementedError("Implementers should subclass CredentialStorageBackend and pass the subclass instance"
                                  " when instantiating RelyingPartyManager.")

    def get_credential_by_id(self, credential_id):
        raise NotImplementedError()

    def get_credential_by_email(self, email):
        raise NotImplementedError()

    def save_credential_for_user(self, email, credential):
        raise NotImplementedError()

class DynamoBackend(CredentialStorageBackend):
    def __init__(self):
        import pynamodb.models, pynamodb.attributes

        class UserModel(pynamodb.models.Model):
            class Meta:
                table_name = "cwa-users"
            email = pynamodb.attributes.UnicodeAttribute(hash_key=True)
            registration_challenge = pynamodb.attributes.BinaryAttribute(null=True)
            authentication_challenge = pynamodb.attributes.BinaryAttribute(null=True)
            credential_id = pynamodb.attributes.BinaryAttribute(null=True)
            credential_public_key = pynamodb.attributes.BinaryAttribute(null=True)
        self.UserModel = UserModel
        self.UserModel.create_table(read_capacity_units=1, write_capacity_units=1, wait=True)

    def get_credential_by_id(self, credential_id):
        raise NotImplementedError()

    def get_credential_by_email(self, email):
        print("Getting user for", email)
        user = self.UserModel.get(email)
        return Credential(credential_id=user.credential_id, credential_public_key=user.credential_public_key)

    def save_credential_for_user(self, email, credential):
        user = self.UserModel(email)
        user.credential_id = credential.id
        user.credential_public_key = credential.public_key.cbor_cose_key
        user.save()

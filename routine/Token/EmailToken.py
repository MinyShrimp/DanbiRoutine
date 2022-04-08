from rest_framework_simplejwt.tokens import RefreshToken

class EmailToken(RefreshToken):
    @classmethod
    def getToken(cls, email):
        token = cls()
        token["email"] = email
        return token
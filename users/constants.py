from enum import Enum,unique
class StrEnum(Enum):
    def __repr__(self) -> str:
        return str(self.value)

    def __str__(self) -> str:
        return self.value
@unique
class AUTH_PROVIDERS(StrEnum):
    FACEBOOK = 'facebook'

AUTH_PROVIDERS.FACEBOOK
TOTP_EXPIRY_TIME = 900
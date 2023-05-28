from enum import Enum


class GoogleOAuthType(str, Enum):
    SERVICE_ACCOUNT: str = "service_account"


class GoogleOAuthURI(str, Enum):
    AUTH: str = "https://accounts.google.com/o/oauth2/auth"
    TOKEN: str = "https://oauth2.googleapis.com/token"
    AUTH_PROVIDER_X509_CERT_URL: str = "https://www.googleapis.com/oauth2/v1/certs"

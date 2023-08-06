from getpass import getpass
from lastpass import Vault
from lastpass.exceptions import (
        LastPassIncorrectGoogleAuthenticatorCodeError,
        LastPassIncorrectYubikeyPasswordError,
        LastPassUnknownError
)
from lastpass_hibp import DEVICE_ID


class LastPassWrapper:
    def __init__(self, username=None, password=None, mfa=False):
        if username is None:
            username = input('LastPass Username: ')
        self.username = username
        if password is None:
            password = getpass('LastPass Password: ')
        self.password = password
        self.mfa = mfa

    def __token(self):
        return  getpass('YubiKey/Authenticator code: ')

    def vault(self):
        multifactor_password = None
        if self.mfa:
            multifactor_password = self.__token()

        try:
            return Vault.open_remote(self.username, self.password, multifactor_password, DEVICE_ID)
        except LastPassIncorrectGoogleAuthenticatorCodeError as _:
            if not self.mfa:
                self.mfa = True
                return self.vault()
        except LastPassIncorrectYubikeyPasswordError as _:
            if not self.mfa:
                self.mfa = True
                return self.vault()
        except LastPassUnknownError as e:
            if 'Multifactor authentication required' in str(e):
                if not self.mfa:
                    self.mfa = True
                    return self.vault()
            else:
                raise e

        return None

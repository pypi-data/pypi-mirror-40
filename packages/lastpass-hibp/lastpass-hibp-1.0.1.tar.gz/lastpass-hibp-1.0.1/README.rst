lastpass-hibp
=============

**lastpass-hibp** is a simple cli tool to check
all the lastpass password if they are leaked
on https://haveibeenpwned.com/ without sending them
the actual password.

Install
~~~~~~~

::

   pip install lastpass-hibp

   # or as a user
   pip install --user lastpass-hibp

Example usage:
~~~~~~~~~~~~~~

::

   ❯ lastpass-hibp --mfa
   LastPass Username: xxxxxx
   LastPass Password: xxxxxx
   YubiKey/Authenticator code: xxxxxx
   Number of accounts: 10
   100% (10 of 10) |#######################| Elapsed Time: 0:00:00 Time:  0:00:00

   ❯ lastpass-hibp --help
   Usage: lastpass-hibp [OPTIONS]

   Options:
     --mfa / --no-mfa  Ask for MFA by default.
     --output TEXT     Output file
     --username TEXT   LastPass Username
     --password TEXT   LastPass Username !!! NOT RECOMMENDED
     --help            Show this message and exit.


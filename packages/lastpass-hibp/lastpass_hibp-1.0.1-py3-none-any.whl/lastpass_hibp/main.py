#!/usr/bin/env python3
# coding: utf-8
import click
from progressbar import ProgressBar
from lastpass_hibp.hibp_checker import check_password
from lastpass_hibp.lastpass_wrapper import LastPassWrapper

class LastPassHIBP:
    def check(arg=None):
        print("check wtf")

@click.command()
@click.option('--mfa/--no-mfa', default=False, help='Ask for MFA by default.')
@click.option('--output', default='lastpass_account_list', help='Output file')
@click.option('--username', default=None, help='LastPass Username')
@click.option('--password', default=None, help='LastPass Username !!! NOT RECOMMENDED')
def run(mfa, output, username, password):
    lpass = LastPassWrapper(username, password, mfa)
    vault = lpass.vault()

    number_of_accounts = len(vault.accounts)
    click.echo("Number of accounts: {:d}".format(number_of_accounts))

    with open(output, 'w') as f:
        with ProgressBar(max_value=number_of_accounts) as bar:
            i = 0
            for account in vault.accounts:
                flag = 'leaked' if check_password(account.password) else ''
                f.write("[{:6s}] <{:s}> {:s} @ {:s}\n".format(
                    flag,
                    account.id.decode(),
                    account.username.decode(),
                    account.name.decode()))
                i += 1
                bar.update(i)


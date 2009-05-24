import sys
import configopt

from isping import helpers
from isping.services import Services

class Main(object):

    def __init__(self):
        self.init_main_config()
        self.init_services()

    def init_services(self):
        self.services = Services()

    def init_main_config(self):
        self.cfg = configopt.ConfigOpt('isping')

        self.cfg.add_group('General', 'General Options')

        self.cfg.add_option('-u', '--username',
            group='General',
            option='username',
            help='Your ISPing username',
            )
        self.cfg.add_option('-p', '--password',
            group='General',
            option='password',
            help='Your ISPing password',
            )

        self.cfg()
        self.main = self.cfg['General']

        return True

    def get_account_details(self, account):
        isp = account['isp.module']
        provider = helpers.get_provider_module(isp)
        print provider
        print provider.get_usage()

    def fetch_accounts(self):
        self.services.post('login',
            username=self.main['username'], 
            password=self.main['password'],
        )
        return self.services.get('accounts')

    def run(self):
        accounts = self.fetch_accounts()
        print accounts
        for account in accounts:
            self.run_account(account)

    def run_account(self, account):
        details = self.get_account_details(account)
        print details



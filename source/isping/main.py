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
        self.debug_config()

        self.main = self.cfg['General']

        return True

    def check_account(self, account):
        try:
            isp = self.cfg[account]['isp']
        except KeyError:
            print('Account %s needs an "isp" config option' % (account))
            sys.exit(1)

        provider = helpers.get_provider_module(isp)
        provider_settings = provider.get_settings()
        for setting in provider_settings:
            if setting.is_required and setting.name not in self.cfg[account]:
                print('Account %s is missing a required setting: %s' % (
                    account, setting.name))
                sys.exit(1)

    def debug_config(self):
        for group_name, group in self.cfg._groups.items():
            print group_name
            for option_name, option in group.options.items():
                print ' -', option_name, '=', option.value

    def get_account_details(self, account):
        isp = account['isp.module']
        provider = helpers.get_provider_module(isp)
#        provider.set_config(self.cfg[account].get_key_value_dict())

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



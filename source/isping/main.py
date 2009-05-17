import sys
import configopt

from isping import helpers

class Main(object):

    def __init__(self):
        self.init_config()

    def init_config(self):
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
        self.cfg.add_option('-a', '--accounts',
            group='General',
            option='accounts',
            help='A comma separated list of accounts',
            )

        self.cfg()
        self.debug_config()

        accounts = self.cfg['General']['accounts'].split(',')
        for account in accounts:
            self.check_account(account)

        return True

    def check_account(self, account):
        try:
            isp = self.cfg[account]['isp']
        except KeyError:
            print('Account %s needs an "isp" config option' % (account))
            sys.exit(1)

        provider = helpers.get_provider_module(isp)
        provider_settings = provider.settings()
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

    def run(self):
        pass


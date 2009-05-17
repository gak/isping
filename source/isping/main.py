import sys
import configopt

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

        self.account_cfg = {}
        accounts = self.cfg['General']['accounts'].split(',')

    def debug_config(self):
        from pprint import pprint
        for group_name, group in self.cfg._groups.items():
            print group_name
            for option_name, option in group.options.items():
                print ' -', option_name, '=', option.value



    def run(self):
        pass


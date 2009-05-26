import os
import sys
import configopt
from getpass import getpass
import json
import ConfigParser

from isping import helpers
from isping.services import Services

class Main(object):

    def __init__(self):
        self.init_main_config()
        self.init_services()
        self.accounts = {}

    def init_services(self):
        self.services = Services(self.main['service_url'])

    def init_main_config(self):
        self.main_cfg = configopt.ConfigOpt('isping')

        self.main_cfg.add_group('General', 'General Options')

        self.main_cfg.add_option('-u', '--username',
            group='General',
            option='username',
            help='Your ISPing username',
            default='',
            )
        self.main_cfg.add_option('-p', '--password',
            group='General',
            option='password',
            help='Your ISPing password',
            default='',
            )
        self.main_cfg.add_option('-s', '--service-url',
            group='General',
            option='service_url',
            help='isping services URI',
            default='http://rarrrr.com/services/',
            )

        self.main_cfg()
        self.main_cfg.save()
        self.main = self.main_cfg['General']

        return True

    def ensure_isping_creds(self):
        if not self.main['username']:
            self.main['username'] = raw_input('isping Username: ')
        if not self.main['password']:
            self.main['password'] = getpass('isping Password: ')
        self.main_cfg.save()

    def ensure_account_creds(self, account):
        print
        print 'Accounts details for account "%s"' % account.name

        # Load up the account config
        sec = 'Settings'
        cfg = ConfigParser.ConfigParser()
        cfg_path = os.path.join(
            self.main_cfg._config_path,
            '%s.account' % account.name,
        )
        cfg.read(cfg_path)
        try:
            cfg.add_section(sec)
        except ConfigParser.DuplicateSectionError:
            pass

        for setting in account.get_settings():
                
            # Get existing value from cfg
            try:
                existing = cfg.get(sec, setting.name, None)
            except ConfigParser.NoOptionError:
                existing = None

            inp = '%s: ' % setting.name

            # Ask the user for the credential/setting
            if setting.is_password:
                if existing:
                    inp = '%s [Enter for saved]: ' % setting.name
                value = getpass(inp)
            else:
                if existing:
                    inp = '%s [%s]: ' % (setting.name, existing)
                value = raw_input(inp)

            # Save the new or existing value
            if value:
                cfg.set(sec, setting.name, value)
            else:
                value = existing

            account.set_config_item(setting.name, value)

        # Save to file
        with open(cfg_path, 'wb') as configfile:
            cfg.write(configfile)

    def fetch_accounts(self):
        self.services.post('login',
            username=self.main['username'], 
            password=self.main['password'],
        )
        for account in self.services.get('accounts'):
            isp = account['isp.module']
            name = account['name']
            provider = helpers.get_provider_instance(isp)
            provider.name = name
            provider.isp = isp
            self.accounts[name] = provider

    def run(self):
        self.ensure_isping_creds()
        accounts = self.fetch_accounts()
        for name, account in self.accounts.items():
            self.ensure_account_creds(account)
            self.run_account(account)

    def run_account(self, account):
        current_usage = account.get_current_usage()
        self.services.post('usage',
            account=account.name,
            data=json.dumps(current_usage),
        )
        print current_usage



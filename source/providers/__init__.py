# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------
# Provider base class
# -----------------------------------------------------------------------------

class Provider(object):

    def set_config_items(self, **d):
        for key, value in d.items():
            self.set_config_item(key, value)

    def set_config_item(self, key, value):
        setattr(self, key, value)


# -----------------------------------------------------------------------------
# Settings
# -----------------------------------------------------------------------------

class Setting(object):

    def __init__(self, name, is_required=False, is_password=False):
        self.name = name
        self.is_required = is_required
        self.is_password = is_password
   
    def __str__(self):
        return self.name


class UserName(Setting):

    def __init__(self):
        Setting.__init__(self, 'username', is_required=True)


class Password(Setting):

    def __init__(self):
        Setting.__init__(self, 'password', is_required=True, is_password=True)
    
    

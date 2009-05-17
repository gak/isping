class Setting(object):

    def __init__(self, name, is_required=True):
        self.name = name
        self.is_required = is_required
   
    def __str__(self):
        return self.name

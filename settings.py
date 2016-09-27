import os
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))

# url: https://code.djangoproject.com/wiki/SplitSettings

# You can key the configurations off of anything - I use project path.
configs = {
    '/home/atty/Prog/2016_ENSG_PYTHON_COURS': 'maison-linux',
}

# Import the configuration settings file - REPLACE projectname with your project
config_module = __import__('config.%s' % configs[ROOT_PATH], globals(), locals(), '2016_ENSG_PYTHON_COURS')

# Load the config settings properties into the local scope.
for setting in dir(config_module):
    if setting == setting.upper():
        locals()[setting] = getattr(config_module, setting)

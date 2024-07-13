import config
from gui import window

config.set_config()  # Create or update config.ini

cfg = config.read_config()  # Get the configurations

App = window.Window(cfg)  # Create the app
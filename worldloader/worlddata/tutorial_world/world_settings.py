"""
Add these at the end of the settings file:

from worlddata import world_settings
INSTALLED_APPS = INSTALLED_APPS + (world_settings.WORLD_DATA_APP,)

"""

import worldloader.world_settings_default

CSV_DATA_FOLDER = "worlddata/tutorial_world"
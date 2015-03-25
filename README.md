It is a tool for Evennia(github.com/evennia/evennia) which can load game world from csv files.

You need to install Evennia and create your game first. Evennia's wiki is here: github.com/evennia/evennia/wiki.

Then, copy folder ```worldloader``` to your game folder, and copy folder ```worldloader/worlddata``` to your game folder too. The directory should look like

----- worlddata
  |
  --- worldloader

Add these at the end of the settings file:
```
from worlddata import world_settings
INSTALLED_APPS = INSTALLED_APPS + (world_settings.WORLD_DATA_APP,)
```
  
Add these to ```CharacterCmdSet```'s ```at_cmdset_creation``` in ```<game folder>/command/default_cmdsets.py```:
```
        self.add(worldloader.command.CmdImportCsv())
        self.add(worldloader.command.CmdBatchBuilder())
        self.add(worldloader.command.CmdSetDataInfo())
```

The ```at_cmdset_creation``` should look like this:
```
    def at_cmdset_creation(self):
        """
        Populates the cmdset
        """
        super(CharacterCmdSet, self).at_cmdset_creation()
        #
        # any commands you add below will overload the default ones.
        #
        self.add(worldloader.command.CmdImportCsv())
        self.add(worldloader.command.CmdBatchBuilder())
        self.add(worldloader.command.CmdSetDataInfo())
```

There are three new commands:
1. ```@importcsv``` It can load data from CSV files to game db. CSV files' path is in ```/worlddata/world_settings.py```'s ```CSV_DATA_FOLDER```.

2. ```@datainfo``` It can set an object's data info in game directly.

3. ```@batchbuild``` It can setup the whole game world with data in CSV files.

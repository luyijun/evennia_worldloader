# Intro
It is a tool for Evennia(github.com/evennia/evennia) which can load game world from csv files.

## Installation
You need to install Evennia and create your game first. Evennia's wiki is here: github.com/evennia/evennia/wiki.

Then, copy folder ```worldloader``` and ```worlddata``` to your game folder. The directory should look like

```
game
  |
  ----- commands  
    |
    --- server
    |
    --- ...
    |
    --- worlddata
    |
    --- worldloader
```

Add these at the end of the settings file:
```
from worlddata import world_settings
INSTALLED_APPS = INSTALLED_APPS + (world_settings.WORLD_DATA_APP,)
```

Run "evennia migrate".
  
Add these to ```CharacterCmdSet```'s ```at_cmdset_creation``` in ```<game folder>/commands/default_cmdsets.py```:
```
import worldloader.command
```

```
        self.add(worldloader.command.CmdImportCsv())
        self.add(worldloader.command.CmdBatchBuilder())
        self.add(worldloader.command.CmdSetDataInfo())
```

The ```at_cmdset_creation``` should look like this:
```
from evennia import default_cmds
import worldloader.command

class CharacterCmdSet(default_cmds.CharacterCmdSet):
    """
    The `CharacterCmdSet` contains general in-game commands like `look`,
    `get`, etc available on in-game Character objects. It is merged with
    the `PlayerCmdSet` when a Player puppets a Character.
    """
    key = "DefaultCharacter"

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

In ```worlddata/world_settings.py```, you can set ```CSV_DATA_FOLDER``` to your CSV files' folder.


## CSV data files
The CSV files (except ```world_details.csv```) have these fields:
```
key,name,alias,typeclass,desc,lock,attributes,location,destination
```

These values will set to object's relative property. Data in ```attributes``` field should be in form of Python's dict. All other fields will be set to object's attributes too.

Objects in ```world_rooms.csv```, ```world_exits.csv```, ```world_objects.csv``` are unique. Every record should has one and only one object in the world.

Objects in ```personal_objects.csv``` are not unique, a record can has zero or multiple objects.

The ```world_details.csv``` is used to set object's detail only.

The values in ```key``` field should be unique in the whole world. The worldloader uses these keys to identify objects, ```location``` and ```destination``` fields also use these keys.


## Install tutorial world
The tutorial world is from Evennia's tutorial world.

Run Evennia and login.

As a builder in game, you should move yourself to Limbo and input:
```
@datainfo #2=.limbo
```
(This adds a unique key to Limbo.)

Then input:
```
@batchbld
```

If everything is OK, the tutorial should be build.


## Use another world
If you want to build another world, you can set ```CSV_DATA_FOLDER``` in ```worlddata/world_settings.py``` to your world data folder.
```
CSV_DATA_FOLDER = "worlddata/your_world"
```

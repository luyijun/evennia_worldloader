"""
Commands

Commands describe the input the player can do to the game.

"""

import os
import django
import loader
from django.conf import settings
from django.db.models.loading import get_model
from evennia.utils import create, search, logger
from worlddata import world_settings


def import_all(caller):
    """
    Import all csv files to db model
    """

    # count the number of files loaded
    count = 0
    
    # get appname
    appname = world_settings.WORLD_DATA_APP

    # import models one by one
    for model_names in world_settings.WORLD_DATA:
        for model_name in model_names:
            # make filename
            filename = os.path.join(world_settings.CSV_DATA_PATH, model_name + ".csv")
            
            # import data
            try:
                loader.import_csv(filename, appname, model_name)
                if caller:
                    caller.msg("%s imported" % model_name)
                count += 1
            except Exception, e:
                if caller:
                    caller.msg(("Can not import %s: %s") % (model_name, e))
                continue

    if caller:
        caller.msg("total %d files imported" % count)



def build_objects(caller, modelname, unique):
    """
    Build objects of a model.
    
    caller: command caller.
    modelname: (string) The name of the data model.
    unique: (boolean) If unique, every record in model should has one and only one object in the world.
                      If not unique, a record can has zero or multiple objects.
    """
    model_obj = get_model(world_settings.WORLD_DATA_APP, modelname)
    
    # new objects
    new_obj_names = set(record.key for record in model_obj.objects.all())

    # current objects
    current_objs = loader.search_obj_info_model(modelname)

    # remove objects
    count_remove = 0
    count_create = 0
    current_obj_keys = set()
    
    for obj in current_objs:
        obj_key = loader.get_info_key(obj)
        
        if unique:
            if obj_key in current_obj_keys:
                # This object is duplcated.
                if caller:
                    caller.msg("Deleting %s" % obj_key)
                obj.delete()
                count_remove += 1
                continue
                
            if not obj_key in new_obj_names:
                # This object should be removed
                if caller:
                    caller.msg("Deleting %s" % obj_key)
                obj.delete()
                count_remove += 1
                continue
        
        # Refresh object.
        loader.load_data(obj)
        current_obj_keys.add(obj_key)

    if unique:
        # Create objects.
        for record in model_obj.objects.all():
            if not record.key in current_obj_keys:
                # Create new objects.
                obj = create.create_object(record.typeclass,
                                           record.name)
                loader.set_obj_data_info(obj, modelname, record.key)
                count_create += 1

    if caller:
        string = "Removed %d object(s). Created %d object(s). Total %d objects." % (count_remove, count_create, len(model_obj.objects.all()))
        caller.msg(string)


def build_details(caller, modelname):
    """
    Build details of a model.
    
    caller: command caller.
    modelname: (string) The name of the data model.
    """
    
    model_detail = get_model(world_settings.WORLD_DATA_APP, modelname)
    
    # Remove all details
    objects = search.search_object_attribute(key="details")
    for obj in objects:
        obj.attributes.remove("details")
    
    # Set details.
    count = 0
    for record in model_detail.objects.all():
        location_objs = loader.search_obj_info_key(record.location)
        
        # Detail's location.
        for location in location_objs:
            loader.set_obj_detail(location, record.name, record.desc);

            for name in record.name.split(";"):
                loader.set_obj_detail(location, name, record.desc);
                
            count += 1

    if caller:
        string = "Set %d detail(s)." % count
        caller.msg(string)


def build_all(caller):
    """
    Load csv data and build the world.
    """
    import_all(caller)

    for room in world_settings.WORLD_ROOMS:
        build_objects(caller, room, True)

    for exit in world_settings.WORLD_EXITS:
        build_objects(caller, exit, True)

    for object in world_settings.WORLD_OBJECTS:
        build_objects(caller, object, True)

    for object in world_settings.PERSONAL_OBJECTS:
        build_objects(caller, object, False)

    for detail in world_settings.WORLD_DETAILS:
        build_details(caller, detail)



"""
This file handles all of the flags/conditionals/variables used by the game to remember stuff
It's pretty much just one dictionary object - might include some file reading or something too

Started by Andrew Curry June 7, 2020 (why do i even include this lul)

TODO needs to be updated to the 7/27 new system/framework/idea

Thoughts about new design:
Individual flags don't need their own class, since all they do is hold one variable. But should there be a single
class/object that holds all of the flags for the GameModel? Or should the GameModel just directly use a dict of all the
flags?

Here's my decision for now - this file will just have code to generate a dict of values for the GameModel, which it will
use directly as its flags. It will look more like the _data files. (maybe I should change the name?)

I'm putting the code inside a FlagDataHandler class for consitency, but it will only have class methods to generate the dict
"""
# imports ------
from game_model.game_objects.room import Room
from enum import Enum

# classes --------


class BasicFlagKeys:
    """
    This is an Enum without being an Enum for the keys for flags that should be in every scenario in order for the game
    to function. I didn't make it an actual Enum because then they won't actually be strings. Maybe I'll stop using Enum
    in general now that I think about it
    """
    REMEMBERED_COMMANDS = "remembered_commands"
    CURRENT_LOCATION = "current_location"
    PROMPT_TEXT_TICKS_LEFT = "input_text_ticks_left"
    EVENT_TEXT_TICKS_LEFT = "event_text_ticks_left"

# end BasicFlagKeys


class FlagDataHandler:
    """
    Holds the logic for loading and saving flag data
    """
    flags = dict()
    flags_loaded = False

    @classmethod
    def load(cls, source: str = "hardcoded"):
        """
        Returns a dict of flags for use by the calling GameModel. Each flag is a single variable (boolean, int, or string?).
        Since the state of flags can actually change over the course of the game, I technically have to prepare for loading
        from a save file here, although I won't actually implement that just yet.
        :param source: indicate the filename to get the current state of flags from.
        :return: the dict of flags (or, False if the load didn't work?
        """

        if FlagDataHandler.flags_loaded:
            print("ERROR: flags have already been loaded")
            # TODO throw exception?
            return False

        if source == "hardcoded":  # this is all more complicated than it needs to be
            FlagDataHandler.flags_loaded = FlagDataHandler.hardcoded_flags()
            if FlagDataHandler.flags_loaded:
                return FlagDataHandler.flags
            else:
                print("ERROR: problem loading hardcoded flags")
                return False
        else:
            print("ERROR: loading flags from", source, "is not yet supported.")
            # TODO throw exception?
    # end load_flags function

    @classmethod
    def save_flags(cls, flags_to_save: dict, filename: str):
        """
        Writes the given flag data to a file with the given filename. NOT YET IMPLEMENTED

        :param flags_to_save: a dict of the flag data to be saved
        :param filename: the name of the file to save the data in.
        :return:
        """
        pass

    @classmethod
    def hardcoded_flags(cls):
        """
        fills the flags dict with these hardcoded flags
        :return: True if all of the flags were loaded properly, False otherwise
        """
        # each of these statements should follow this format:
        # include_flag(<flag key>, <flag starting value>)
        
        def include_flag(key: str, value):
            """
            This is a special version of include to save me time and avoid repeating the same information. This version
            handles instantiating the flag itself. This one is a little different because flag loading is different.

            :param key: the key for the new flag
            :param value: the starting value of the new flag
            :return:
            """

            if key in FlagDataHandler.flags:
                print("ERROR: attempt to add flag with duplicate key", key)
                # TODO actually throw exception or something
            else:
                FlagDataHandler.flags[key] = value

        # basic / critical / whatever flags
        include_flag(BasicFlagKeys.REMEMBERED_COMMANDS,
                     ["test_dance_cmd", "quit_cmd", "test_toggle_cmd", "test_look_at_toggle_cmd",
                      "test_rm_3_toggle_cmd", "didnt_understand_cmd"])
        include_flag(BasicFlagKeys.CURRENT_LOCATION, "test_rm_1")
        include_flag(BasicFlagKeys.EVENT_TEXT_TICKS_LEFT, -1)  # for now use -1 as the "don't change it" value
        include_flag(BasicFlagKeys.PROMPT_TEXT_TICKS_LEFT, -1)

        # room layer flags
        include_flag("test_rm_1" + Room.ROOM_FLAG_SUFFIX, 0)
        include_flag("test_rm_2" + Room.ROOM_FLAG_SUFFIX, 0)
        include_flag("test_rm_3" + Room.ROOM_FLAG_SUFFIX, 0)

        # test flags
        include_flag("test_toggle", False)

        # we got to the end
        return True
    # end hardcoded_flags function
# end FlagDataHandler class

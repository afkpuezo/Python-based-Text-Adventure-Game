"""
This file handles getting all of the actual data for commands in the game. Currently they are just hardcoded in, I might
change it to reading from some kind of file later. Ultimately it just returns a dict of all the commands.

started 7/28/20 blah blah blah
code put into a class on 7/29/20 - wish me luck
"""
# imports ---------
from game_model.game_objects.command import Command
from game_model.game_objects.command import PatElm
# from utilities.load_util import include

# from typing import Dict


class CommandDataHandler:
    """
    This class has a class-level method that contains the code for loading the command-related scenario data. I put it
    into a class to make importing and using it in the GameModel cleaner.
    """

    # class-level variables
    commands_loaded = False

    @classmethod
    def load(cls, setup: str = "default") -> dict:
        """
        This function loads all of the commands for this scenario (duh).
        Will probably get really long at some point, as every event will be defined inside this function, unless I switch
        implementations.

        :param setup: might be used to designate filename or something like that
        :return: the dict of all Commands for the scenario (or returns False if failure)
        """

        # TODO is this necessary? idk it just feels like it will be easier to change later
        if setup != "default":
            print("ERROR: non-default setup for commands not yet implemented")
            # TODO actual exception
            return False

        if CommandDataHandler.commands_loaded:
            print("ERROR: commands already loaded")
            # TODO exception
            return False

        # commands = Dict[str, Command] FIXME also return type
        commands = dict()
        
        def include_command(key: str, event_key: str, pattern: list):
            """
            This is a special version of include to save me time and avoid repeating the same information. This version
            handles instantiating the command itself.

            :param key: the key for the new command
            :param event_key: the key for the event triggered by the new command
            :param pattern: the pattern this command is looking for
            :return:
            """

            if key in commands:
                print("ERROR: attempt to add command with duplicate key", key)
                # TODO actually throw exception or something
            else:
                commands[key] = Command(key, event_key, pattern)

        # begin command definition ---------
        # basic / utility / critical commands ---------------------
        include_command("didnt_understand_cmd", "didnt_understand_ev", [PatElm.ANY_NONE_OKAY])
        include_command("quit_cmd", "quit_ev", ["quit", PatElm.END])

        # test commands -------------
        include_command("test_1_to_2_cmd", "test_1_to_2_ev", ["move", PatElm.END])
        include_command("test_2_to_3_cmd", "test_2_to_3_ev", ["move", PatElm.END])
        include_command("test_3_to_1_cmd", "test_3_to_1_ev", ["move", PatElm.END])
        include_command("test_dance_cmd", "test_dance_ev", [["dance", "jig", "celebrate"], PatElm.END])
        include_command("test_toggle_cmd", "test_toggle_ev", ["toggle", PatElm.END])
        include_command("test_look_at_toggle_cmd", "test_look_at_toggle_ev", ["look", "at", "toggle", PatElm.END])
        include_command("test_rm_3_toggle_cmd", "test_rm_3_toggle_ev", ["check", "toggle", "3", PatElm.END])

        # we got to the end...
        CommandDataHandler.commands_loaded = True
        return commands

    # end load function

# end CommandDataHandler class


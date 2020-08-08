"""
This file handles getting all of the actual data for descs in the game. Currently, they are just hardcoded in; I might
change it to reading from some kind of file later. Ultimately it just returns a dict of all the descs.

started 7/28/20 blah blah blah
turned into a class 7/29/20
"""
# imports ----------
from game_model.game_objects.desc import Desc
# from utilities.load_util import include we're using a special include here to save time

# from typing import Dict  # not 100% on how this works


class DescDataHandler:
    """
    This class has a class-level method that contains the code for loading the event-related scenario data. I put it
    into a class to make importing and using it in the GameModel cleaner.
    """

    # class-level variable
    descs_loaded = False

    @classmethod
    def load(cls, setup: str = "default") -> dict():
        """
        This function loads all of the descs for this scenario (duh).
        Will probably get really long at some point, as every desc will be defined inside this function, unless I switch
        implementations.

        :param setup: might be used to designate filename or something like that
        :return: the dict of Descs, or False if failure
        """

        # TODO is this necessary? idk it just feels like it will be easier to change later
        if setup != "default":
            print("ERROR: non-default setup for descs not yet implemented")
            # TODO actual exception
            return False

        if DescDataHandler.descs_loaded:
            print("ERROR: descs already loaded")
            # TODO exception
            return False

        # begin desc definition --------------------
        # descs = Dict[str, Desc] FIXME ahhhhhhhh return type
        descs = dict()

        def include_desc(key: str, text: str, has_condition: bool = False):
            """
            This is a special version of include to save me time and avoid repeating the same information. This version
            handles instantiating the desc itself.

            :param key: the key for the new desc
            :param text: the text for the new desc
            :param has_condition: whether the text has condition(s) in it. Defaults to False
            :return:
            """

            if key in descs:
                print("ERROR: attempt to add room with duplicate key", key)
                # TODO actually throw exception or something
            else:
                descs[key] = Desc(key, text, has_condition)

        # end include method

        # utility / basic / critical Descs
        include_desc("blank_desc", "")
        include_desc("default_main_text_desc", "This is the default main text.")
        include_desc("default_event_text_desc", "")
        include_desc("default_prompt_text_desc", "What will you do?")
        include_desc("didnt_understand_desc", "I didn't understand that.")

        include_desc("initial_main_text_desc", "This the initial main text.")
        include_desc("initial_event_text_desc", "")
        include_desc("initial_prompt_text_desc", "")

        # "specific" descs - rooms, events, etc FOR TESTS --------------------
        include_desc("test_rm_1_desc", "This is the main text for test room 1.")
        include_desc("test_rm_2_desc", "This is the main text for test room 2.")
        include_desc("test_rm_3_desc", "This is the main text for test room 3.")

        include_desc("test_ev_1_to_2_desc", "This is the event text for moving from test room 1 to test room 2.")
        include_desc("test_ev_2_to_3_desc", "This is the event text for moving from test room 2 to test room 3.")
        include_desc("test_ev_3_to_1_desc", "This is the event text for moving from test room 3 to test room 1.")
        include_desc("test_ev_dance_desc",
                     "You do a jig 'cuz your code works. [current_location == test_rm_3 :Yay!|No, you're in <current_location>]", True)
        include_desc("test_look_at_toggle_desc",
                     "Value of toggle: <test_toggle>, [test_toggle == True:cool!|lame.]", True)
        include_desc("test_rm_3_toggle_desc",
                     "room 3 AND toggle? [current_location == test_rm_3,test_toggle == True :Both are true. ]Nice."
                     , True)

        DescDataHandler.descs_loaded = True
        return descs
    # end load method


# end DescDataHandler class
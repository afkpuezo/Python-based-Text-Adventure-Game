"""
This file holds the PCGameModel class. It's possible that the model won't require porting, just the view, but I don't
know what else to call this class. It inherits/implements the GameModel class/interface.

Started 7/29/20
"""
# imports
from game_model.game_model import GameModel
from utilities.game_enums import TextLocationKey
# from game_controller.game_controller import GameController

from game_model.game_objects.command import Command
from game_model.game_objects.desc import Desc
from game_model.game_objects.event import Event
from game_model.game_objects.room import Room
# from game_model.game_objects.room import RoomLayer

from scenario_data.flag_data import FlagDataHandler
from scenario_data.flag_data import BasicFlagKeys
from scenario_data.command_data import CommandDataHandler
from scenario_data.room_data import RoomDataHandler
from scenario_data.event_data import EventDataHandler
from scenario_data.desc_data import DescDataHandler


from typing import Dict  # not 100% on how this works
from typing import List


class PCGameModel(GameModel):
    """
    Models the actual game state, using Rooms, flags, Commands, Descs, Events, etc. This version is intended for the PC
    version of the game but I'm not sure how much porting work will have to be done on this portion of the code (or if I
    really intend to port the game at all)

    Extends/implements GameModel. Interacts with GameController.

    TODO more thorough description?
    """

    # begin GameModel stuff -------

    def game_launched(self) -> Dict[str, str]:
        """
        What to do when the game is launched/opened. Returns the initial texts to be displayed.

        :return:
        """
        self.load_scenario_data()  # TODO i assume this will change later
        return self.texts
    # end game_launched

    def player_quit(self):
        """
        What to do when the user is quitting. Takes care of business in the model and tells the controller. (Currently)
        called by the quit event.

        :return:
        """
        self.playing = False  # is this still important?
        self.controller.player_quit()
    # end player_quit

    def load_scenario_data(self, scenario: str = "default"):
        """
        Load the starting data for the given scenario - rooms, flags, events, commands, descs, etc.

        :param scenario: The name (or filename?) of the scenario to be loaded
        :return: True if load successful, False otherwise
        """

        if scenario != "default":
            print("PCGameModel is only able to load the default scenario!")
            # TODO make an actual exception
            return False

        # assume scenario is default
        self.data_loaded = self.load_default_scenario()  # helper method

        return self.data_loaded

    # end load_scenario_data method

    def load_save_file(self, filename):
        """
        Load the flag data from the given save file

        :param filename: the name of the save file
        :return:
        """
        print("PCGameModel load_save_file not yet implemented")

    def game_start(self) -> dict:
        """
        Indicates that gameplay can start. Called by the game controller to allow actual gameplay logic to begin.

        Right now, this checks to see if data has actually been loaded, then, if so, it sets the internal 'playing'
        instance variable to True, then wait for input

        :return: the initial texts to show to the player (or false if game couldn't start)
        """
        if self.data_loaded:
            self.playing = True
            # load the text information for the current/starting room before looping
            self.change_text(TextLocationKey.MAIN, self.get_current_room_desc_key())
            self.change_text(TextLocationKey.EVENT, "initial_event_text_desc")
            self.change_text(TextLocationKey.PROMPT, "initial_prompt_text_desc")
            # self.draw_all_output_text()
            return self.texts
        else:
            print("ERROR PCGameModel was asked to game_start without a successful load!")
            # TODO exception?
            return False
    # end game_start method

    def set_controller(self, controller):
        """
        Called by the controller to connect itself to the model.
        (I don't know if this is necessary but it seems safer?)

        :param controller: The GameController
        :return:
        """
        self.controller = controller
    # end set_controller method

    # begin PCGameModel stuff ----------

    DEFAULT_STARTING_TEXT = ""

    def __init__(self):
        """
        The constructor. Declares instance variables for the game objects but does not fill them (load_scenario_data
        does that).
        """

        # game logic variables/objects - why am I stressing about what order to declare these in?
        self.all_rooms: dict = Dict[str, Room]
        self.all_flags: dict = dict()  # FIXME can you specify only the key type?
        self.all_commands: dict = Dict[str, Command]
        # self.remembered_command_key_keys: list = list()  # TODO consider renaming this?
        self.all_events : dict = Dict[str, Event]
        self.all_descs : dict = Dict[str, Desc]

        # these store what text is shown to to the player
        #self.texts = Dict[TextLocationKey, str] FIXME maybe?
        self.texts = dict()
        self.texts[TextLocationKey.MAIN] = PCGameModel.DEFAULT_STARTING_TEXT
        self.texts[TextLocationKey.EVENT] = PCGameModel.DEFAULT_STARTING_TEXT
        self.texts[TextLocationKey.PROMPT] = PCGameModel.DEFAULT_STARTING_TEXT

        # non-game logic variables/objects
        self.controller: GameController = None  # will be set directly by the controller itself
        self.data_loaded = False  # has data been loaded yet?
        self.playing = False  # indicates if the game is started and the player is able to do things in-game

    # end constructor

    def load_default_scenario(self):
        """
        A helper method for the load_scenario_data method from the GameModel interface. Uses the default and/or
        hardcoded data for the game objects.
        :return: True if the load worked, False otherwise # TODO may not actually work yet
        """

        self.all_rooms = RoomDataHandler.load()
        self.all_flags = FlagDataHandler.load()
        self.all_commands = CommandDataHandler.load()

        # this is a separate function because it can be called when loading from a save file as well
        # self.load_remembered_command_key_keys()

        self.all_events = EventDataHandler.load()
        self.all_descs = DescDataHandler.load()

        return True  # assumes that the load was successful if we get here...
        # TODO implement actual checking to see if the load was successful
    # end load_default_scenario method

    def append_remembered_command_key(self, cmd_key: str):
        """
        Appends the given command to the list of remembered commands. If the command is already remembered, the list
        will not be modified.

        :param cmd_key: the key of the command to be added
        :return: Whether or not the command was added
        """
        remembered_command_keys = self.get_remembered_command_keys()

        if cmd_key in remembered_command_keys:
            return False
        else:
            remembered_command_keys.append(cmd_key)
            return True
    # end add_remembered_command_key method

    def remove_remembered_command_key(self, cmd_key: str):
        """
        Removes the given command from the list of remembered commands. If the command is not remembered, the list will
        not be modified.

        :param cmd_key: the key of the command to be removed
        :return: Whether or not the command was removed
        """
        remembered_command_keys = self.get_remembered_command_keys()

        if cmd_key in remembered_command_keys:
            remembered_command_keys.remove(cmd_key)
            return True
        else:
            return False
    # end remove_remembered_command_key method

    def get_remembered_command_keys(self):
        """
        I read a thing that if you repeat the same code 3 times, you should make it a function/method, so here we are.

        :return: A list of keys corresponding to the currently remembered commands.
        """
        return self.all_flags[BasicFlagKeys.REMEMBERED_COMMANDS]
    # end get_remembered_command_keys method

    def update(self, input_text: str):
        """
        The core gameplay logic. Called by the controller when there's input to be processed.

        :return: The dict of texts that should be shown on-screen
        """

        # now we generate the list of commands to check the input against - including the commands associated with
        # the current room, and the remembered commands
        active_commands: List[Command] = list()

        # boy this is a spicy mess isn't it
        current_room: Room = self.all_rooms[self.all_flags[BasicFlagKeys.CURRENT_LOCATION]]
        room_command_keys: list = current_room.get_commands(self.all_flags[current_room.layer_flag_key])
        for room_cmd_key in room_command_keys:
            active_commands.append(self.all_commands[room_cmd_key])

        remembered_command_keys = self.get_remembered_command_keys()
        for rem_cmd_key in remembered_command_keys:
            active_commands.append(self.all_commands[rem_cmd_key])

        # now parse the input based on those commands, getting the appropriate event
        next_event_key: str = Command.find_match(input_text, active_commands).event_key
        self.trigger_event(next_event_key, input_text)

        # now do the (experimental) update event to do bookkeeping
        self.trigger_event("update_ev", input_text)  # TODO enum-ify the key?

        # we need this to actually see any changes
        # self.draw_all_output_text()
        return self.texts

    # end update method

    def get_current_room_desc_key(self) -> str:
        """
        Finds the Desc object associated with the current layer of the current room. This is a helper method for the
        gameplay_loop method, because I made getting this information take several steps because I'm a silly man
        TODO should this method be declared inside update?

        :return: the Desc object associated with the current layer of the current room
        """
        current_room: Room = self.all_rooms[self.all_flags[BasicFlagKeys.CURRENT_LOCATION]]  # boy this is convoluted
        layer_flag = self.all_flags[current_room.layer_flag_key]
        return current_room.get_desc_key(layer_flag)
    # end get_current_room_desc method

    def change_text(self, loc_key: TextLocationKey, desc_key: str, ticks_left: int = -2):
        """
        Updates the text to be displayed in a single location. It's possible that this method is superfluous and that
        the texts dict could be accessed directly, but it just feels right to have this extra bit of control.

        :param loc_key: the key indicating which text location is being updated
        :param desc_key: the key for the Desc object containing the new text
        :param ticks_left: How many game loops/ticks until the text field will be reverted to the default. Currently ignored
        for the main text area. Set it to -1 to make the change permanent. Set it to -2 to not change the current state.
        :return:
        """

        if ticks_left != -2:
            if loc_key == TextLocationKey.EVENT:
                self.all_flags[BasicFlagKeys.EVENT_TEXT_TICKS_LEFT] = ticks_left
            elif loc_key == TextLocationKey.PROMPT:
                self.all_flags[BasicFlagKeys.PROMPT_TEXT_TICKS_LEFT] = ticks_left

        self.texts[loc_key] = self.all_descs[desc_key].get_output(self.all_flags)
    # end change_text method

    def move_to_room(self, room_key: str):
        """
        Changes the current_room to the given room (key). This is a method in case any special effects happen when you
        change rooms.

        :param room_key: the key of the destination room
        :return:
        """
        self.all_flags[BasicFlagKeys.CURRENT_LOCATION] = room_key
        self.change_text(TextLocationKey.MAIN, self.get_current_room_desc_key())
    # end move_to_room

    def trigger_event(self, event_key: str, input_text: str):
        """
        Triggers the do_event subfunction of the Event corresponding to the given key.

        :param event_key: The key for the event
        :param input_text: The input that caused the event to be triggered (in case it's needed)
        :return:
        """
        self.all_events[event_key].do_event(self, input_text)
    # end trigger_event

    def is_playing(self):
        """
        Called by the controller to determine if the game has been quit.

        :return: True if gameplay will continue, False otherwise
        """
        return self.playing
    # end is_playing method
# end PCGameModel class
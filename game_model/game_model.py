"""
This file will contain the GameModel, used to...model the game model in the model/controller/view framework. Technically
this is an abstract class and/or informal interface, which will be implemented by specific game models for flexibility.

TODO should the controller ask the model for text, or should the model tell the controller when text changes? I'm going
TODO to have the model call the controller when text changes

started 7/28/20 by Andrew Curry
"""


class TextLocationKey: # TODO these need to move to a different file or something, too many different things use them
    """
    An Enum* for the keys that indicate where text is to be shown
    """
    MAIN = "MAIN_TEXT_LOCATION"
    EVENT = "EVENT_TEXT_LOCATION"
    PROMPT = "PROMPT_TEXT_LOCATION"
    INPUT = "INPUT_TEXT_LOCATION"
# end TextLocationKey


class GameModel:

    """
    An informal interface that describes what game models will need to implement.

    TODO description
    """

    def game_launched(self):
        """
        What to do when the game is launched/opened.
        TODO necessary?

        :return:
        """
        pass

    def game_closing(self):
        """
        What to do when the user is quitting.
        TODO necessary?

        :return:
        """
        pass

    def load_scenario_data(self, scenario: str = "default"):
        """
        Load the starting data for the given scenario - rooms, flags, events, commands, descs, etc.

        :param scenario: The name (or filename?) of the scenario to be loaded
        :return:
        """
        pass

    def load_save_file(self, filename):
        """
        Load the flag data from the given save file

        :param filename: the name of the save file
        :return:
        """
        pass

    def game_start(self) -> dict:
        """
        Indicates that gameplay can start. Called by the game controller to allow actual gameplay logic to begin

        :return: the initial texts to show to the player (or false if game couldn't start)
        """
        pass

    def game_stop(self):
        """
        Indicates that gameplay will stop. Caled by the game controller to end/pause gamemplay logic
        :return:
        """
        pass

    def update(self, input_text: str):
        """
        The core gameplay logic. Called by the controller when there's input to be processed.
        :return:
        """
        pass

    def is_playing(self):
        """
        Called by the controller to determine if the game has been quit.

        :return: True if gameplay will continue, False otherwise
        """
        pass

# end class GameModel

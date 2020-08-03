"""
This file has the TestController class - a GameController that uses the console to print text.

started 7/29/20
"""
# imports
from game_controller.game_controller import GameController
from game_model.game_model import TextLocationKey
from game_model.pc_game_model import PCGameModel
from game_model.game_model import GameModel


class TestController(GameController):
    """
    An implementation of GameController that uses the console to print text. Used for testing the GameModel without
    having to implement the GameView just yet.

    TODO should this have to be instantiated? when are you going to have more than one? just to be safe i guess
    """

    # stuff from GameController -----------

    def game_launched(self):
        """
        What to do when the game is launched. Currently, tells the model to load scenario data, and then starts the
        game, letting the test 'loop' run once and then ending the game.

        :return:
        """
        self.model.load_scenario_data()
        self.print_text(self.model.game_start())

        while self.model.is_playing():
            # get the input and pass it
            input_text = input("INPUT:")
            output_text = self.model.update(input_text)
            self.print_text(output_text)

        self.game_closing()
    # end game_launched method

    def game_closing(self):
        """
        What to do when the game is being closed/quit by the player.

        :return:
        """
        print("Game over.")

    def print_text(self, texts: dict):
        """
        Prints out this text. Implementation different in real controllers.

        :param texts: A dict of the text to be displayed. Each key is for one of the text display locations, and the
        corresponding value is the text to be displayed in that location.
        :return:
        """
        print("---------------------------------")
        print("MAIN TEXT:", texts[TextLocationKey.MAIN], "\n")
        print("EVENT TEXT:", texts[TextLocationKey.EVENT], "\n")
        print("PROMPT TEXT:", texts[TextLocationKey.PROMPT])
        print("---------------------------------")
    # end print_text method


    # stuff from TestController (for?) ------------

    def __init__(self):
        """
        The constructor. Initializes the GameModel
        """
        self.model : GameModel = PCGameModel(self)
        # is this really all I need?
    # end constructor

# end TestController class

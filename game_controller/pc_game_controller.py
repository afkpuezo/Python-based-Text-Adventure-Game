"""
This file contains the "real" controller that I'll use for the game (at least for now). As usual I've called it PC but
I don't know if it will actually require much porting. You should instantiate it and pass it the Model and View?

Started 08/05/20, by Andrew Curry
"""
# imports
from game_controller.game_controller import GameController
from game_view.game_view import GameView
from game_model.game_model import GameModel

from typing import Dict

# actual code


class PCGameController(GameController):
    """
    This class handles the controller role in the Model/Controller/View setup. It inherits/extends the informal
    interface/abstract class GameView.

    Currently I think it has very little to do, just create the model/view and carry text between them. I'm sure that
    will change as soon as I discover how many mistakes I've made.
    """

    # GameController stuff
    def game_launched(self):
        """
        What to do when the game is launched. I'm still not sure if these are necessary.

        :return:
        """
        self.model.game_launched()
        initial_texts: Dict[str, str] = self.model.game_start()
        self.view.game_launched(initial_texts)
    # end game_launched

    def player_quit(self):
        """
        What to do when the game is being closed/quit by the player. This one should be called by the model when the
        player has chosen to quit.

        :return:
        """
        self.view.game_closing()
    # end player_quit method

    def send_input_text_to_model(self, input_text: str) -> Dict[str, str]:
        """
        Sends the given input text to the GameModel (calls the update method). Returns the dict of text(s) to be
        displayed on screen.

        :param input_text: the input text typed by the player
        :return: the updated output text(s)
        """
        return self.model.update(input_text)
    # end send_input_text_to_model method

    # PCGameController stuff

    def __init__(self, model: GameModel, view: GameView):
        """
        The constructor. Will call set_controller of both model and view

        :param model: the GameModel object
        :param view: the GameView object
        """
        self.model: GameModel = model
        self.view: GameView = view

        self.model.set_controller(self)
        self.view.set_controller(self)
    # end constructor

# end PCGameController class

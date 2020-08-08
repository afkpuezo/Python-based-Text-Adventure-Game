"""
This file contains the informal interface / abstract class for game views - GameView. It will be implemented/inherited
by other classes.

started  08/01/20
"""
from typing import Dict

class GameView:
    """
    the informal interface / abstract class for game views - GameView. It will be implemented/inherited
    by other classes.
    """

    def game_launched(self, output_texts: Dict[str, str]):
        """
        What to do when the game is launched.
        TODO is this the right way to split this up?

        :param output_texts: The initial text to be displayed
        :return:
        """
        pass

    def game_closing(self):
        """
        What to do when the user quits. TODO IDK if this is even a thing

        :return:
        """
        pass

    def set_controller(self, controller):
        """
        Called by the controller to connect itself to the view.
        (I don't know if this is necessary but it seems safer?)

        :param controller: The GameController
        :return:
        """
        pass
# end GameView class

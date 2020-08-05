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

    def game_launched(self, output_text: Dict[str, str]):
        """
        What to do when the game is launched.
        TODO is this the right way to split this up?

        :return:
        """
        pass

    def game_closing(self):
        """
        What to do when the user quits. TODO IDK if this is even a thing

        :return:
        """
        pass
# end GameView class

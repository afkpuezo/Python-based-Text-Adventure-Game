"""
This is a placeholder for the game controller logic/class/whatever - it will be filled in later. I'm just putting this
here while I write the PCGameModel class.

7/29/20
"""
from typing import Dict


class GameController:
    """
    An informal interface / abstract class for game controllers. Actual implementation handled by child classes.
    """

    def game_launched(self):
        """
        What to do when the game is launched.

        :return:
        """
        pass

    def game_closing(self):
        """
        What to do when the game is being closed/quit by the player.

        :return:
        """
        pass

    def send_input_text_to_model(self, input_text: str) -> Dict[str, str]:
        """
        Sends the given input text to the GameModel (calls the update method). Returns the dict of text(s) to be
        displayed on screen.

        :param input_text: the dict of text(s) to be displayed on screen.
        :return:
        """
        pass
# end GameController class/interface/whatever

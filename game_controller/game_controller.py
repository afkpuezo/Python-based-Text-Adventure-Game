"""
This is a placeholder for the game controller logic/class/whatever - it will be filled in later. I'm just putting this
here while I write the PCGameModel class.

7/29/20
"""


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


# end GameController class/interface/whatever

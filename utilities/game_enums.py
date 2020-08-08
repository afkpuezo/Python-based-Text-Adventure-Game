"""
This file contains psuedo-enums that need to be accessed from too many different, disparate places (like the model and
the view) so I decided to put them in one place

Started 08/06/20, Andrew
"""


class TextLocationKey:
    """
    An enum* for the keys that indicate where text is to be shown, used by model and view
    """
    MAIN = "MAIN_TEXT_LOCATION"
    EVENT = "EVENT_TEXT_LOCATION"
    PROMPT = "PROMPT_TEXT_LOCATION"
    INPUT = "INPUT_TEXT_LOCATION"
# end TextLocationKey

"""
This module contains the Desc class, used to contain all of the in-game text that can be displayed on-screen. The name
'Desc' is a reference to escape velocity; it's the most fitting name I can think of that isn't just 'text'.

TODO think about and eventually implement conditionals in descs - EG to handle different items being present in a room
TODO without having to resort to new rooms/layers, etc

TODO potential conflict with pre-existing 'desc' - is it just for sorting in descending order?

Notes:
- going to update this to be an actual class.
- need access to the flags for conditional stuff - or the whole game_model?.
"""


class ConditionChars:
    """
    used in Desc get_output
    """

    OPEN_BRACKET = '['  # maybe this is overkill
    CLOSE_BRACKET = ']'
    TEXT_START = ':'  # marks when the conditions end and the text starts
    ALT_OUTPUT_START = '|'
# end DescConditionalChars class


class ConditionOperators:
    """
    used in Desc get_output
    """

    EQUALS = '=='
    NOT_EQUALS = '!='
# end ConditionOperators class


class FlagInsertChars:
    """
    used in Desc get_output
    """
    OPEN_BRACKET = '<'
    CLOSE_BRACKET = '>'
# end FlagInsertChars class

class Desc:

    """
    Represents/encapsulates/whatever blocks of text for the game. Each Desc object determines what its output should be
    when requested, based on the current state of the game flags.
    TODO (Implementation of that pending - subclasses? patterns like commands? EV style embedded in the text itself?)

    Also contains utilily class methods
    """

    # class-level stuff --------

    # instance-level stuff ----------

    def __init__(self, key: str, text: str, has_condition: bool = False):
        """
        The constructor.

        :param key: the unique string identifier for this Desc object
        :param text: the string text contained by this Desc object (or, the 'value' of this Desc)
        :param has_condition: Set this to True if the text in this Desc has conditions. Will default to False
        """

        self.key :str = key
        self.text :str = text
        self.has_condition: bool = has_condition
    # end constructor

    def get_output(self, flags: dict = []) -> str:
        """
        Called by the GameModel to determine the actual text output of this Desc. Is given access to the current state
        of the GameModel's flags in case there is some kind of condition in this Desc (EG, if an item is still present)

        :param flags: a dictionary of the flags and their current state in the game. The Desc may check certain flags in
        order to determine its output.
        :return: the text to be outputted to the screen/player
        """
        if not self.has_condition:
            return self.text
        else:
            output = str()
            # i have to use this bool to control whether i do this at the end of the loop because helpers are being dumb
            try_to_write = False
            inside_bracket = False  # TODO really need to nail down names
            reading_conditions = False
            raw_conditions = ""
            conditions_result = False
            in_alt_text = False
            reading_flag = False
            raw_flag_key = ""

            def evaluate_conditions():
                """
                A helper method used to parse the text conditions and determine if the bracketed text should be
                displayed.

                :return: The result of ANDing all the conditions.
                """
                all_conditions = raw_conditions.split(',')
                # print(all_conditions)
                for cond in all_conditions:
                    if evaluate(cond):  # helpers in helpers
                        pass # keep looping
                    else:
                        return False  # one False is enough

                return True  # if we got to the end, there are no Falses
            # end evaluate_conditions method

            def evaluate(cond: str):
                """
                This might be too many helpers

                :param cond: the string of a single condition
                :return: Whether this single condition is True or False
                """
                cond_split = cond.split(" ")
                flag_key = cond_split[0]
                operator = cond_split[1]
                value = cond_split[2] # if there's a trailing space there will be a [3] but we don't need it?

                if operator == ConditionOperators.EQUALS:
                    return str(flags[flag_key]) == value  # important to str() the flag
                elif operator == ConditionOperators.NOT_EQUALS:
                    return str(flags[flag_key]) != value
                else:
                    print("ERROR: operator '", operator, ", not recognized for output in Desc", self.key)
                    return False  # TODO exception instead?
            # end evaluate

            for ch in self.text:
                if inside_bracket:
                    if reading_conditions:  # reading the conditions
                        if ch == ConditionChars.TEXT_START:  # time to parse and evaluate the conditions
                            reading_conditions = False
                            conditions_result = evaluate_conditions()  # helper method for clarity
                        else:  # reading the conditions
                            raw_conditions = raw_conditions + ch
                    else:  # reading the text itself
                        if ch == ConditionChars.ALT_OUTPUT_START:
                            in_alt_text = True
                        elif ch == ConditionChars.CLOSE_BRACKET:
                            # this means we've gotten to the end of this expression; reset everything
                            inside_bracket = False
                            raw_conditions = str()
                            conditions_result = False
                            in_alt_text = False
                        elif conditions_result and (not in_alt_text):
                            # output = output + ch
                            try_to_write = True
                        elif (not conditions_result) and in_alt_text:
                            # output = output + ch
                            try_to_write = True
                        else:
                            pass  # if nothing should be printed
                else:  # if not inside_bracket
                    # we're currently reading normal text, so unless we see a '[', just add the char to output
                    if ch == ConditionChars.OPEN_BRACKET:
                        inside_bracket = True
                        reading_conditions = True
                    else:
                        # output = output + ch
                        try_to_write = True
                # end of all the ifs
                if try_to_write:  # now we have to check for flag insertion, or just add ch to output directly
                    if reading_flag:
                        if ch == FlagInsertChars.CLOSE_BRACKET:
                            output += str(flags[raw_flag_key])
                            raw_flag_key = ""
                            reading_flag = False
                        else: # part of the flag key
                            raw_flag_key += ch
                    elif ch == FlagInsertChars.OPEN_BRACKET:
                        reading_flag = True
                    else:  # just append a normal char
                        output += ch
                    # no matter what, reset for next loop
                    try_to_write = False
            # end for loop

            return output
    # end get_output function

# end class Desc



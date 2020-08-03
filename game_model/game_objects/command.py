"""
This file is for code relating to commands - they connect an expected input pattern to an in-game effect.

- Started 5/25/20, by Andrew Curry
- reworked 7/28/20, to put the text parsing logic in here, as well as minor refactoring and including how command data
        is loaded
"""
# imports ------
from enum import Enum
# from scenario_data import command_data # obviously this is bad lul


# helper code/classes/variables/etc


class PatElm:

    """
    Stands for Pattern Elements. TODO consider renaming?
    These are keywords (ish) used to give instructions to the text parsing logic.
    """
    ANY_ONE_WORD = "_ANY_ONE_WORD"  # any ONE word will satisfy this part of the pattern
    ANY_AT_LEAST_ONE_WORD = "_ANY_AT_LEAST_ONE_WORD"  # as long as there is at least an element in this position,
                                                        # any input will satisfy this condition
    ANY_NONE_OKAY = "_ANY_NONE_OKAY"  # the parser will confirm any input once it gets to this element of the pattern
                                        # - even if there is nothing
    ANY_ALPHA = "_ANY_ALPHA"  # any word without numeric characters
    ANY_NUMBER = "_ANY_NUMBER"  # any 'word' with only numeric characters (0 - 9)
    ANY_CHARACTER = "_ANY_CHARACTER"  # any single character
    ANY_LETTER = "_ANY_LETTER"  # any single letter character
    ANY_DIGIT = "_ANY_DIGIT"  # any single numerical digit character

    END = "_END"  # make sure the input is done
# end PatElm enum class


class Command:

    """
    The Command class, essetinally representing input that the game (through rooms) anticipates the player to input.
    Each command object has: a command-key for itself (string?), an event-key for the event it triggers (string?), and
    a list representing a pattern of expected input
    """

    # class-level stuff ------------

    @classmethod
    def find_match(cls, input_text: str, commands: list): # TODO can't specify list of commands?
        """
        Takes the user's text and finds the first command it matches in the list.

        :param input_text: the player's input text
        :param commands: the possible commands the game is expecting right now. They will be checked in order; if there
        are multiple matches only the first is returned. There should be a catch-all ("i didn't understand that")
        command at the end.
        :return: the FIRST command that matches what the player input.

        TODO maybe i'll have it raise an exception if the list runs out
        """
        # convert the text string to a list
        input_list = input_text.split() # TODO make this it's own function if things get more complicated
        # check each command
        for cmd in commands:
            matched = cmd.check_input(input_list)
            if matched:
                return cmd  # return the right command
        # end find_match function -----------------------------------------------

    # instance-level stuff ----------

    def __init__(self, key: str, event_key: str, pattern: list = []):
        """
        The constructor.

        :param key:  the unique identifier for this command (string?)
        :param event_key: the unique identifier for the event triggered by this command (string?)
        :param pattern:  a list representing a pattern of expected input, used to see if the user's text input matches
        """
        self.key = key # do they need to know their own keys?
        self.event_key = event_key
        self.pattern = pattern

        # end init ------------------------------------------

    def __str__(self):
        """
        The to-string method.

        :return a string representation of this object
        """
        return "<(" + str(self.key) + " " + str(self.event_key) + ")" + " " + str(self.pattern) + ">"
        # end __str__ function

    def check_input(self, input_list: list):  # TODO how to indicate list of only strings?

        """
        Determines if the given player input matches with this command. NOTE: this was transferred from another module
        so there may be problems with this code later. TODO

        :param input_list: a list of strings, each string being a word from the player's input
        :return: True if the given input matches this command, False otherwise
        """
        # basically keep going through the input and command until we find something that doesn't match
        # or if we find certain escape sequences in the command (like ANY)

        #pattern = command.pattern
        p_length = len(self.pattern) # does this actually save time?
        input_length = len(input_list)

        # print("DEBUG check_command pattern is:", pattern)
        # print("DEBUG check_command input_list is:", input_list)

        for i in range(0, p_length):
            p = self.pattern[i]  # the current pattern element #TODO better name than p?

            if p == PatElm.ANY_NONE_OKAY:
                return True

            # see if the input is not long enough
            if i >= input_length:
                return p == PatElm.END  # is it supposed to be the end?

            # we know there's at least one word left
            if p == PatElm.ANY_AT_LEAST_ONE_WORD:
                return True

            if p == PatElm.ANY_ONE_WORD:
                continue  # we're good so far, keep checking

            # now we can safely get the current word
            word = input_list[i]

            if p == PatElm.ANY_CHARACTER:
                if len(word) == 1:
                    continue
                else:
                    return False

            if p == PatElm.ANY_LETTER:
                if len(word) == 1 and word.isalpha():
                    continue
                else:
                    return False

            if p == PatElm.ANY_DIGIT:
                if len(word) == 1 and word.isdigit():
                    continue
                else:
                    return False

            if p == PatElm.ANY_ALPHA:
                # print("DEBUG: got to if p == ANY_ALPHA, word is:", word)
                if word.isalpha():
                    continue
                else:
                    return False

            if p == PatElm.ANY_NUMBER:
                if word.isdigit():
                    continue
                else:
                    return False

            # at this point we're only looking for exact matches
            # print("DEBUG got to the exact word check - p and word are:", p, word)
            if p.lower() == word.lower():
                continue
            else:
                return False
            # end for loop

        return True  # if we get to the end, we haven't found a problem yet
    # end check_input method

# end class Command

# test functions TODO do these belong here?


def test_text_parsing():

    """
    what it looks like

    :return:
    """
    commands = list()
    commands.append(Command('c1', 'e1', ['go', 'dennis', PatElm.END]))
    commands.append(Command('c2', 'e2', ['go', 'dennis', PatElm.ANY_AT_LEAST_ONE_WORD]))
    commands.append(Command('c3', 'e3', ['get', 'ye', 'flask', PatElm.ANY_NONE_OKAY]))
    commands.append(Command('c4', 'e4', [PatElm.ANY_NUMBER, 'swag', PatElm.END]))
    commands.append(Command('c5', 'e5', [PatElm.ANY_CHARACTER, PatElm.ANY_LETTER, PatElm.ANY_DIGIT, PatElm.ANY_NONE_OKAY]))
    commands.append(Command('c_end', 'e_end', [PatElm.ANY_NONE_OKAY]))

    for cmd in commands:
        print(cmd)

    print("\n\n\n\n")

    input1 = "go dennis"
    print(input1 + " " + str(Command.find_match(input1, commands)))

    input2 = "go dennis again okay just do it"
    print(input2 + " " + str(Command.find_match(input2, commands)))

    input3 = "get ye flask"
    print(input3 + " " + str(Command.find_match(input3, commands)))

    input4 = "420 swag"
    print(input4 + " " + str(Command.find_match(input4, commands)))

    input5 = "a b 3 afsdklfasdjkfasfd"
    print(input5 + " " + str(Command.find_match(input5, commands)))

    input6 = "this should fail"
    print(input6 + " " + str(Command.find_match(input6, commands)))

    input7 = "a a a a a a a a"
    print(input7 + " " + str(Command.find_match(input7, commands)))
# end test_input_parsing function

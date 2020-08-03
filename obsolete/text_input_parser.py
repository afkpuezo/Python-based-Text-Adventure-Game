"""
This file is for the code that takes player text input and matches it up with expected game commands

not sure if it should be a class you instantiate or be procedural
The basic idea is that the game will pass the player's text input and a list of expected commands, and the parser will
    try to find the best match

-Started 5/25/20, by Andrew Curry
-reworked 7/28/20 by Andrew Curry - all functionality rolled into Command class, should make this module obsolete
"""
# imports etc ---------------------------------------------------------------------------------------------------------
from game_model.game_objects.command import Command as Command

# global variables, etc -----------------------------------------------------------------------------------------------

# pattern elements -----------
# escape sequence -ish strings/characters used in parsing, they form elements of a pattern
# they will use characters not allowed in player input
# maybe these should be in a different file, who knows # TODO
ANY_ONE_WORD = "_ANY_ONE_WORD" # any ONE word will satisfy this part of the pattern
ANY_AT_LEAST_ONE_WORD = "_ANY_AT_LEAST_ONE_WORD" # as long as there is at least an element in this position, any input
                                                 # will satisfy this condition
ANY_NONE_OKAY = "_ANY_NONE_OKAY" # the parser will confirm any input once it gets to this element of the pattern - even
                                 # if there is nothing
ANY_ALPHA = "_ANY_ALPHA" # any word without numeric characters
ANY_NUMBER = "_ANY_NUMBER" # any 'word' with only numeric characters (0 - 9)
ANY_CHARACTER = "_ANY_CHARACTER" # any single character
ANY_LETTER = "_ANY_LETTER" # any single letter character
ANY_DIGIT = "_ANY_DIGIT" # any single numerical digit character

END_PATTERN = "_END" # make sure the input is done


# functions -----------------------------------------------------------------------------------------------------------

# find_match function -----------------------------------------------------
def find_match(text, commands):
    """
    takes the user's text and finds the first command it matches in the list
    :param text: the player's input text
    :param commands: the possible commands the game is expecting right now
                     they will be checked in order; if there are multiple matches only the first will be returned
                     there should be a catch-all (error) command at the end
    :return: the FIRST command that matches what the player input

    maybe i'll have it raise an exception if the list runs out
    """
    # convert the text string to a list
    input_list = text.split()
    # check each command
    for cmd in commands:
        matched = check_command(input_list, cmd)
        if matched:
            return cmd # return the right command
    # end find_match function -----------------------------------------------

def check_command(input_list, command):
    """
    checks to see if the given input_list matches up to the given command
    :param input_list:
    :param command:
    :return: true if it does match up, false if it doesnt
    """

    # basically keep going through the input and command until we find something that doesn't match
    # or if we find certain escape sequences in the command (like ANY)

    pattern = command.pattern
    p_length = len(pattern)
    input_length = len(input_list)

    # print("DEBUG check_command pattern is:", pattern)
    # print("DEBUG check_command input_list is:", input_list)

    for i in range(0, p_length):
        p = pattern[i] # the current pattern element #TODO better name than p

        if p == ANY_NONE_OKAY:
            return True

        # see if the input is not long enough
        if i >= input_length:
            return p == END_PATTERN # is it supposed to be the end?

        # we know there's at least one word left
        if p == ANY_AT_LEAST_ONE_WORD:
            return True

        if p == ANY_ONE_WORD:
            continue # we're good so far, keep checking

        # now we can safely get the current word
        word = input_list[i]

        if p == ANY_CHARACTER:
            if len(word) == 1:
                continue
            else:
                return False

        if p == ANY_LETTER:
            if len(word) == 1 and word.isalpha():
                continue
            else:
                return False

        if p == ANY_DIGIT:
            if len(word) == 1 and word.isdigit():
                continue
            else:
                return False

        if p == ANY_ALPHA:
            # print("DEBUG: got to if p == ANY_ALPHA, word is:", word)
            if word.isalpha():
                continue
            else:
                return False

        if p == ANY_NUMBER:
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


    return True # if we get to the end, we haven't found a problem yet
    # end check_command function -------------------------------------------


def test():

    """
    what it looks like
    :return:
    """
    commands = list()
    commands.append(Command('c1', 'e1', ['go', 'dennis', END_PATTERN]))
    commands.append(Command('c2', 'e2', ['go', 'dennis', ANY_AT_LEAST_ONE_WORD]))
    commands.append(Command('c3', 'e3', ['get', 'ye', 'flask', ANY_NONE_OKAY]))
    commands.append(Command('c4', 'e4', [ANY_NUMBER, 'swag', END_PATTERN]))
    commands.append(Command('c5', 'e5', [ANY_CHARACTER, ANY_LETTER, ANY_DIGIT, ANY_NONE_OKAY]))
    commands.append(Command('c_end', 'e_end', [ANY_NONE_OKAY]))

    for cmd in commands:
        print(cmd)

    print("\n\n\n\n")

    input1 = "go dennis"
    print(input1 + " " + str(find_match(input1, commands)))

    input2 = "go dennis again okay just do it"
    print(input2 + " " + str(find_match(input2, commands)))

    input3 = "get ye flask"
    print(input3 + " " + str(find_match(input3, commands)))

    input4 = "420 swag"
    print(input4 + " " + str(find_match(input4, commands)))

    input5 = "a b 3 afsdklfasdjkfasfd"
    print(input5 + " " + str(find_match(input5, commands)))

    input6 = "this should fail"
    print(input6 + " " + str(find_match(input6, commands)))

    input7 = "a a a a a a a a"
    print(input7 + " " + str(find_match(input7, commands)))
    # end test function

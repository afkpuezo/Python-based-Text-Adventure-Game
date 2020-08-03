"""
This file handles the event class - the code/scripts that are executed when commands are processed.
What should events be able to do?
    -change current room
    -change game flags
    -execute other events?
    -print text to screen?

Events should also have the ability to evaluate conditions during their execution to modify their effect - EG only
change rooms if certain flags have been met.

Also, I'm using this as a test run of my new architecture for these game object classes and how they are organized in
the code.

This will include...
    -this file will include the actual class modeling events
    -that class will have a class method that returns a dict of all events in use for the current scenario
    -the data for all of the events will be loaded in a seperate file (?), but currently it is just a .py file with
                all of the events

Also I started this at 1:47 AM July 28 2020 but who cares

Notes and thoughts:
    -should this be called something like GameEvent to disambiguate it? idk man i should just start working
    -oh shit should events just be standalone functions? idk dawg
    -maybe need a better name for do_event
    -do they need to know their own key?
    -should they know what room they're associated with?
    -maybe do_event only needs to know the flags, not the whole game model? idk
    -should do_event return anything?
"""
# imports ----------
from typing import Callable
from game_model.game_model import GameModel
# from game_model.game_objects.command import Command
# from scenario_data import event_data


class Event:

    """
    Represents in-game events that can be triggered by player commands.
    Also has some static methods for support.

    The important part of an Event object is the do_event function, which is the actual important code and is
    requested and triggered by the GameModel.
    """

    # class stuff -------

    # instance stuff -------

    def __init__(self, key: str, do_event: Callable[[GameModel, str], None]):
        """
        The constructor, should only really be called during setup/loading. The do_event subfunction gets the input_text
        in case it needs to modify its execution based on what the input was.
        TODO this functionality could be covered by having multiple command/events - necessary?

        :param key: a unique string identifier for this event
        :param do_event: the function that is called when this event is triggered, which should have the following
                        parameters: game_model, input_text. They should have no return (or None?)
        """

        self.key = key
        self.do_event = do_event
    # end constructor

# end Event class --------

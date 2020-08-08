"""
This file handles getting all of the actual data for events in the game. Currently, they are just hardcoded in, I might
change it to reading from some kind of file later. Ultimately it just returns a dict of all the events.

started 7/28/20 blah blah blah
put into a class 7/29/20
"""
# imports --------
from game_model.game_objects.event import Event
from utilities.game_enums import TextLocationKey
from scenario_data.flag_data import BasicFlagKeys

# from typing import Dict
from typing import Callable


class EventDataHandler:
    """
    This class has a class-level method that contains the code for loading the event-related scenario data. I put it
    into a class to make importing and using it in the GameModel cleaner.
    """

    # class-level variable
    events_loaded = False

    @classmethod
    def load(cls, setup: str = "default") -> dict:
        """
        This function loads all of the events for this scenario (duh).
        Will probably get really long at some point, as every event will be defined inside this function, unless I switch
        implementations.

        :param setup: might be used to designate filename or something like that
        :return: True if the load worked, false otherwise #TODO necessary?
        """

        # TODO is this necessary? idk it just feels like it will be easier to change later
        if setup != "default":
            print("ERROR: non-default setup for events not yet implemented")
            # TODO actual exception
            return False

        if EventDataHandler.events_loaded:
            print("ERROR: events already loaded")
            # TODO exception
            return False

        # begin event definition --------------------
        # events = Dict[str, Event] FIXME also return type
        events = dict()

        def include_event(key: str, do_event: Callable):
            """
            This is a special version of include to save me time and avoid repeating the same information. This version
            handles instantiating the event itself. The do_event function still has to be created seperately (for now?)

            :param key: the key for the new event
            :param do_event: the subfunction for this event
            :return:
            """

            if key in events:
                print("ERROR: attempt to add event with duplicate key", key)
                # TODO actually throw exception or something
            else:
                events[key] = Event(key, do_event)

        # TODO this is a little clumsy cuz I'm actually defining the do_event function of the event
        # basic / critical / utility events ---------------------------------------------------------
        def update_ev(model, input_text: str):
            """
            This event is called at the end of every game loop to do maintenance.

            :param model:
            :param input_text:
            :return:
            """

            event_text_ticks_left: int = model.all_flags[BasicFlagKeys.EVENT_TEXT_TICKS_LEFT]
            if event_text_ticks_left == 0:  # time to change
                model.change_text(TextLocationKey.EVENT, "default_event_text_desc", -1)
                event_text_ticks_left = -1
            elif event_text_ticks_left > 0:  # not done yet, just tick
                event_text_ticks_left = event_text_ticks_left - 1
            model.all_flags[BasicFlagKeys.EVENT_TEXT_TICKS_LEFT] = event_text_ticks_left  # saves the change

            input_text_ticks_left: int = model.all_flags[BasicFlagKeys.PROMPT_TEXT_TICKS_LEFT]
            if input_text_ticks_left == 0:  # time to change
                model.change_text(TextLocationKey.PROMPT, "default_prompt_text_desc", -1)
                input_text_ticks_left = -1
            elif input_text_ticks_left > 0:  # not done yet, just tick
                input_text_ticks_left = input_text_ticks_left - 1
            model.all_flags[BasicFlagKeys.PROMPT_TEXT_TICKS_LEFT] = input_text_ticks_left  # saves the change
        # end update_ev
        include_event("update_ev", update_ev)

        def didnt_event(model, input_text: str):
            model.change_text(TextLocationKey.PROMPT, "didnt_understand_desc", 1)
        include_event("didnt_understand_ev", didnt_event)

        def quit_event(model, input_text: str):
            model.player_quit()  # TODO this will be more complicated later
        include_event("quit_ev", quit_event)

        # test events -------------------------------------------------------------

        def test_dance_event(model, input_text: str):
            model.change_text(TextLocationKey.EVENT, "test_ev_dance_desc", 1)
        include_event("test_dance_ev", test_dance_event)

        def test_1_to_2_ev(model, input_text: str):
            model.move_to_room("test_rm_2")
        include_event("test_1_to_2_ev", test_1_to_2_ev)

        def test_2_to_3_ev(model, input_text: str):
            model.move_to_room("test_rm_3")
        include_event("test_2_to_3_ev", test_2_to_3_ev)

        def test_3_to_1_ev(model, input_text: str):
            model.move_to_room("test_rm_1")
        include_event("test_3_to_1_ev", test_3_to_1_ev)

        def test_toggle_ev(model, input_text: str):
            model.all_flags["test_toggle"] = not model.all_flags["test_toggle"]
        include_event("test_toggle_ev", test_toggle_ev)

        def test_look_at_toggle_ev(model, input_text: str):
            model.change_text(TextLocationKey.EVENT, "test_look_at_toggle_desc", 1)
        include_event("test_look_at_toggle_ev", test_look_at_toggle_ev)

        def test_rm_3_toggle_ev(model, input_text: str):
            model.change_text(TextLocationKey.EVENT, "test_rm_3_toggle_desc", 1)
        include_event("test_rm_3_toggle_ev", test_rm_3_toggle_ev)


        # we got to the end
        EventDataHandler.events_loaded = True
        return events
    # end load method

# end EventDataHandler class

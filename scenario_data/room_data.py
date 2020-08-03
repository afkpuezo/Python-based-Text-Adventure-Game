"""
This file handles getting all of the actual data for rooms in the game. Currently, they are just hardcoded in, I might
change it to reading from some kind of file later. Ultimately it just returns a dict of all the rooms.

started 7/28/20 blah blah blah
turned into a class 7/29/20
"""
# imports -----
from game_model.game_objects.room import Room
from game_model.game_objects.room import RoomLayer
# from utilities.load_util import include

# from typing import Dict


class RoomDataHandler:
    """
    This class has a class-level method that contains the code for loading the Room-related scenario data. I put it
    into a class to make importing and using it in the GameModel cleaner.
    """

    # class-level variable
    rooms_loaded = False

    @classmethod
    def load(cls, setup: str = "default") -> dict:
        """
        This function loads all of the rooms for this scenario (duh). It will probably get really long at some point, as
        every room will be defined inside this function, unless I switch implementations.

        :param setup: might be used to designate filename or something like that
        :return: the dict of Rooms (or, False if failure)
        """

        # TODO is this necessary? idk it just feels like it will be easier to change later
        if setup != "default":
            print ("ERROR: non-default setup for rooms not yet implemented")
            # TODO actual exception
            return False

        if RoomDataHandler.rooms_loaded:
            print("ERROR: rooms already loaded")
            # TODO exception
            return False

        # begin room definition --------------------
        # rooms = Dict[str, Room] FIXME why is this not working (also return type)
        rooms = dict()
        
        def include_room(key: str, layers: list):
            """
            This is a special version of include to save me time and avoid repeating the same information. This version
            handles instantiating the room itself. This one isn't quite as handy cuz layers, but it still helps.

            :param key: the key for the new room
            :param layers: the Layers for the new room
            :return:
            """

            if key in rooms:
                print("ERROR: attempt to add room with duplicate key", key)
                # TODO actually throw exception or something
            else:
                rooms[key] = Room(key, layers)

        # TODO this is going to be clumsy - have to define all of the layers of a room individually
        test_room_1_layer_0 = RoomLayer("test_rm_1_desc", ["test_1_to_2_cmd"])
        include_room("test_rm_1", [test_room_1_layer_0])

        test_room_2_layer_0 = RoomLayer("test_rm_2_desc", ["test_2_to_3_cmd"])
        include_room("test_rm_2", [test_room_2_layer_0])

        test_room_3_layer_0 = RoomLayer("test_rm_3_desc", ["test_3_to_1_cmd"])
        include_room("test_rm_3", [test_room_3_layer_0])

        # we got to the end
        RoomDataHandler.rooms_loaded = True
        return rooms
    # end load method
# end RoomDataHandler class

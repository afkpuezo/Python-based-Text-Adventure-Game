"""
This file handles the Room class - locations inside the game the player can interact with.
(I might use these in a way that doesn't line up one-to-one with physical rooms in the narrative of the game)

There will be a dictionary of Room objects - each Room will have a number of properties.
For now the setup will be hard-coded, but I might make it read from a file or something later on.

TODO needs to be updated to the 7/27 framework
TODO layers necessary? not sure if they're reduntant or not

TODO should the current layer of each room be represented as a flag? or both? I'm going to have it be a flag, which will
TODO require interaction with the GameModel. THis way all of the save data will be in flags
"""
# imports ------
# from scenario_data import room_data


# ---------- The Room class -----------------------------


class Room:

    """
    Represents rooms inside the game (* might not line up one-to-one with physical rooms in the game narrative).
    Each room is identified by a key and has at least 1 Layer (another class with the actual properties of the room).
    """

    # class-level stuff

    # used by each room to generate the name of the flag that holds information on the current layer
    ROOM_FLAG_SUFFIX = "_current_layer"

    # instance-level stuff

    def __init__(self, key: str, layers: list):
        """
        The constructor.

        :param key: the unique string identifier of this room
        :param layers: a list of layers (different states this room can have)
        """

        self.key = key
        self.layer_flag_key = key + Room.ROOM_FLAG_SUFFIX
        self.layers = layers
        # end constructor

    def get_commands(self, layer_flag: int):
        """
        Get the list of keys for the current Commands of this room.
        TODO does this have to be a function rather than having the layers be directly accessed? idk

        :param layer_flag: the flag that controls this room's current layer. Should be an int index
        :return: the list of keys of Commands
        """
        return self.layers[layer_flag].command_keys
        # end get_commands method

    def get_desc_key(self, layer_flag: int) -> str:
        """
        Returns the key of Desc object of the current layer of this room.
        TODO maybe use properties to hide this and other aspects of layers from the outside?

        :param layer_flag: the flag that controls this room's current layer. Should be an int index
        :return: the key of the Desc object
        """

        return self.layers[layer_flag].desc_key
    # end Room class


class RoomLayer:

    """
    The state of an individual room can change, so we have layers which a room can change between. Each layer has all of
    the useful properties of a room (which may or may not change from other layers in the room).So far those properties
    are:
        -desc
        -possible commands
        -and whatever else I think of later
    """

    def __init__(self, desc_key: str, command_keys: list):
        """
        The constructor. (Note: layers used to have keys, but I don't see the need anymore)

        :param desc_key: The key for the Desc object holding the display text for this room.
        :param commands: The list of expected commands the player can do in this room.
        """

        self.desc_key = desc_key
        self.command_keys = command_keys
    # end __init__ method

    # end Room_Layer class

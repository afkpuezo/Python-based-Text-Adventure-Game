"""
This file contains utility function(s) for the various _data modules. I dunno if this is strictly necessary. Also it's
such a generic name, there might already be a module like this out there somewhere.

started 7/28/20
"""

def include(d: dict, key, elm):
    """
    A helper function for the various load functions - makes sure there are no events with duplicate keys.
    Will throw an 'error' if you attempt to include elements with the same key.
    #TODO make this an actual exception

    :param d: the dictionary to add the new element to
    :param key: the key for the new element
    :param elm: the value of the new element
    :return:
    """
    if key in d:
        print("ERROR: attempt to add event with duplicate key", key)
        # TODO actually throw exception or something
    else:
        d[key] = elm

# end include function
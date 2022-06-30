def unpack(input_tuple):
    #       if `sub` is tuple, use it or use list(sub) -> [[], (), []]
    comp = [isinstance(sub, tuple) and sub or [sub] for sub in input_tuple]
    #      unpack iterable from iterable to tuple
    return tuple(element for sublist in comp for element in sublist)

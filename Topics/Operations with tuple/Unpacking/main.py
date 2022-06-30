def unpack(input_tuple):
    return tuple(
        # first `for` to unpack comprehension
        element for sublist in
        (
            # if `sub` is tuple, use it or use list(sub) -> [[], (), []]
            [isinstance(sub, tuple) and sub or [sub] for sub in input_tuple]
        )
        # second `for` to unpack sub-list/sub-tuple
        for element in sublist
    )

    # or easier way but with more ;) lines

    # u = []
    # for item in input_tuple:
    #     if isinstance(item, tuple):
    #         for i in item:
    #             u.append(i)
    #     else:
    #         u.append(item)
    # return tuple(u)

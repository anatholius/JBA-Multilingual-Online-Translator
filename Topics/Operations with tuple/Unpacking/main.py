def unpack(input_tuple):
    return (
        item if isinstance(item, tuple) else item
        for item in input_tuple
     )
    
    u = []
    for item in input_tuple:
        if isinstance(item, tuple):
            for i in item:
                u.append(i)
        else:
            u.append(item)
    return tuple(u)

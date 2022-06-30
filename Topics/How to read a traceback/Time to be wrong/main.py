def print_list(some_list):
    i = 0
    while i < len(some_list):
        if int(some_list[i]) % 2 == 0:
            print(some_list[i])
        if int(some_list[i]) % 3 == 0:
            print(some_list[i] % 3)
        i += 1

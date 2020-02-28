def print_statistics(arr):
    if len(arr) == 0:
        for n in range(5):
            print(0)
    else:
        print(len(arr))
        print(sum(arr) / len(arr))
        print(arr.sort()[0])
        print(arr.sort()[len(arr) - 1])
        if len(arr) % 2 == 0:
            print((arr.sort()[len(arr) / 2 - 1] + arr.sort()[len(arr) / 2]) / 2)
        else:
            print(arr.sort()[(len(arr) - 1) / 2]

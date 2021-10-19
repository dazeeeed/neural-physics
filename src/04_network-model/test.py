def checkio(array: list) -> int:
    """
        sums even-indexes elements and multiply at the last
    """
    a = []
    if array:
        for i in array:
            if array.index(i) == 0 or array.index(i) % 2 == 0:
                a.append(i)
        print(a)
        return sum(a) * array[-1]
    else:
        return 0


# These "asserts" using only for self-checking and not necessary for auto-testing
if __name__ == '__main__':
    print('Example:')
    lst = [-37, -36, -19, -99, 29, 20, 3, -7, -64, 84, 36, 62, 26, -76, 55, -24, 84, 49, -65, 41]
    print(lst.index(84))
    print(checkio(lst))
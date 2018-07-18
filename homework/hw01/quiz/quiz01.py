def multiple(a, b):
    """Return the smallest number n that is a multiple of both a and b.

    >>> multiple(3, 4)
    12
    >>> multiple(14, 21)
    42
    """
    product = 1
    k = 1
    while product % a != 0 or product % b != 0:
        product = a * k
        k += 1
    return product

def unique_digits(n):
    """Return the number of unique digits in positive integer n

    >>> unique_digits(8675309) # All are unique
    7
    >>> unique_digits(1313131) # 1 and 3
    2
    >>> unique_digits(13173131) # 1, 3, and 7
    3
    >>> unique_digits(10000) # 0 and 1
    2
    >>> unique_digits(101) # 0 and 1
    2
    >>> unique_digits(10) # 0 and 1
    2
    """

    len_n = len(str(n))
    numbers_in_n = []
    while n > 0:
        last_number = n % 10
        n = n // 10 
        last_number_of_rest = n % 10
        numbers_in_n.append(last_number)
    index = 0
    trues = []
    numbers_tried = []
    while index < len_n:
        first_number = numbers_in_n[index]
        if first_number in numbers_tried:
            trues.append(False)
        else:
            trues.append(True)
        numbers_tried.append(first_number)
        index += 1
    return sum(trues)




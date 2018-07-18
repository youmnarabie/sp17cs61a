from utils import *

# Q1
from math import sqrt
def distance(city1, city2):
    """
    >>> city1 = make_city('city1', 0, 1)
    >>> city2 = make_city('city2', 0, 2)
    >>> distance(city1, city2)
    1.0
    >>> city3 = make_city('city3', 6.5, 12)
    >>> city4 = make_city('city4', 2.5, 15)
    >>> distance(city3, city4)
    5.0
    """
    lat_city1 = get_lat(city1)
    lat_city2 = get_lat(city2)
    lon_city1 = get_lon(city1)
    lon_city2 = get_lon(city2)
    return sqrt((lon_city1 - lon_city2) ** 2 + (lat_city1 - lat_city2) ** 2)

# Q2
def closer_city(lat, lon, city1, city2):
    """
    Returns the name of either city1 or city2, whichever is closest to
    coordinate (lat, lon).

    >>> berkeley = make_city('Berkeley', 37.87, 112.26)
    >>> stanford = make_city('Stanford', 34.05, 118.25)
    >>> closer_city(38.33, 121.44, berkeley, stanford)
    'Stanford'
    >>> bucharest = make_city('Bucharest', 44.43, 26.10)
    >>> vienna = make_city('Vienna', 48.20, 16.37)
    >>> closer_city(41.29, 174.78, bucharest, vienna)
    'Bucharest'
    """
    lon_city1 = get_lon(city1)
    lon_city2 = get_lon(city2)
    lat_city1 = get_lat(city1)
    lat_city2 = get_lat(city2)
    distance_from_point_city_1 = sqrt((lon - lon_city1) ** 2 + (lat - lat_city1) ** 2)
    distance_from_point_city_2 = sqrt((lon - lon_city2) ** 2 + (lat - lat_city2) ** 2)
    min_distance = min(distance_from_point_city_1, distance_from_point_city_2)
    if min_distance == distance_from_point_city_1:
        return get_name(city1)
    elif min_distance == distance_from_point_city_2:
        return get_name(city2)

# Q3
def ab_plus_c(a, b, c):
    """Computes a * b + c.

    >>> ab_plus_c(2, 4, 3)  # 2 * 4 + 3
    11
    >>> ab_plus_c(0, 3, 2)  # 0 * 3 + 2
    2
    >>> ab_plus_c(3, 0, 2)  # 3 * 0 + 2
    2
    """
    original_a = a
    if a == 0 or b == 0:
        return c
    else:
        return a + ab_plus_c(a, b - 1, c)

# Q4
def is_prime(n):
    """Returns True if n is a prime number and False otherwise.

    >>> is_prime(2)
    True
    >>> is_prime(16)
    False
    >>> is_prime(521)
    True
    """
    if n == 2:
        return True
    potential_factor = 2
    def changing_factors(potential_factor):
        while potential_factor < n:
            if n % potential_factor == 0:
                return False
            elif n % potential_factor != 0:
                return changing_factors(potential_factor + 1)
        return True
    return changing_factors(potential_factor)


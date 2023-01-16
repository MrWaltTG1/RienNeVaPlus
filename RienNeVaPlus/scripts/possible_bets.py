# Roulette wheel clockwise goes:
wheel = 32, 15, 19, 4, 21, 2, 25, 17, 34, 6, 27, 13, 36, 11, 30, 8, 23, 10, 5, 24, 16, 33, 1 ,20, 14, 31, 9, 22, 18, 29, 7, 28, 12, 35, 3, 26, 0

# 1:1
rouge = 1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36
noir = 2, 4, 6, 8, 10, 11, 13, 15, 17, 20, 22, 24, 26, 28, 29, 31, 33, 35
manque = range(1, 19)  # lower half
passe = range(19, 37)  # upper half
pair = range(2, 37, 2)  # even
impair = range(1, 37, 2)  # uneven

# 1:2
premiere = range(1, 13)  # 1/3
moyenne = range(13, 25)  # 2/3
derniere = range(25, 37)  # 3/3

colonne1 = range(1, 37, 3)
colonne2 = range(2, 37, 3)
colonne3 = range(3, 37, 3)

# 1:5


def transversale_simple(start_number):
    # start_number shouldnt be higher than 31
    value = range(start_number, start_number+6)
    return value

# 1:8


def carre(start_number):
    # start_number shouldnt be higher than 32
    if start_number == 0:
        value = 0, 1, 2, 3
    else:
        value = start_number, start_number+1, start_number+3, start_number+4
    return value

# 1:11


def transversale_pleine(start_number, extra=None):
    if extra:
        value = 0, 2, extra
    else:
        value = range(start_number, start_number+3)
    return value

# 1:17


def cheval(start_number, extra):
    return start_number, extra
# 1:35


def plein(start_number):
    return start_number

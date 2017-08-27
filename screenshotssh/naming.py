import random


def generate_random_name(length):
    name = []
    for _ in range(length):
        index = random.randint(1, len(RANDOM_CHARS)) - 1
        name.append(RANDOM_CHARS[index])
    return "".join(name)


def generate_random_chars():
    chars = []
    for x in range(ord('a'), ord('z') + 1):
        char = chr(x)
        chars.extend([char, char.upper()])
    return chars


RANDOM_CHARS = generate_random_chars()


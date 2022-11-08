import random

def random_hex(n):
    return hex(random.randint(0, (16**n)-1))[2:].zfill(n)

def randomize_case(c):
    match random.randint(0, 3):
        case 0:
            return c.lower()
        case 1:
            return c.upper()
        case 2:
            return c
        case 3:
            return c


def leetify(c):
    match c:
        case "a":
            return "4"
        case "i":
            return "1"
        case "e":
            return "3"
        case "o":
            return "0"
        case "s":
            return "5"
        case "t":
            return "7"
        case "g":
            return "6"
        case _:
            return c


def generate(title: str, text: str, hex_bits=0, random_case=True, leet=True, random_leet=False, join_with_underscore=True):
    new_text = []
    for c in text:
        new_w = ""
        if c == " ":
            if join_with_underscore:
                new_w += "_"
            else:
                new_w += c
        else:
            if random_case:
                c = randomize_case(c)
            if leet:
                if random_leet:
                    match random.randint(0, 1):
                        case 0:
                            new_w += c
                        case 1:
                            new_w += leetify(c)
                else:
                    new_w += leetify(c)
        new_text.append(new_w)
    
    if hex_bits != 0:
        new_text.append("_" + random_hex(hex_bits))

    return title + "{" + "".join(new_text) + "}"

def generate_text(text: str, random_case=True, leet=True, random_leet=True, join_with_underscore=True):
    new_text = []
    for c in text:
        new_w = ""
        if c == " ":
            if join_with_underscore:
                new_w += "_"
            else:
                new_w += c
        else:
            if random_case:
                c = randomize_case(c)
            if leet:
                if random_leet:
                    match random.randint(0, 1):
                        case 0:
                            new_w += c
                        case 1:
                            new_w += leetify(c)
                else:
                    new_w += leetify(c)
        new_text.append(new_w)

    return "".join(new_text)

def format_flag(title: str, text: str, hex_bits: str=""):
    return title + "{" + text + "_" + hex_bits + "}"
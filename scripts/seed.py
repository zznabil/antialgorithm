#!/usr/bin/env python3
import argparse
import random
import sys

import history

rng = random.SystemRandom()
RECENT = {}


def load_recent(kind, seeds=12):
    RECENT.clear()
    same_kind = [e for e in history.load("seed") if e.get("kind") == kind]
    for entry in reversed(same_kind[-seeds:]):
        for axis, value in entry.get("seed", {}).items():
            RECENT.setdefault(axis, [])
            if value not in RECENT[axis]:
                RECENT[axis].append(value)


def pick(axis, items):
    avoid = set(RECENT.get(axis, [])[: len(items) // 2])
    fresh = [i for i in items if i not in avoid]
    return rng.choice(fresh or items)

METHOD_FAMILIES = {
    "hand and print": [
        "woodcut", "screen print", "rubber stamp", "spray stencil", "cut paper collage",
        "photocopy zine", "gouache", "ink brush", "ballpoint sketch", "marker on cardboard",
        "embroidery", "hand painted shop sign", "children's crayon drawing", "spray paint graffiti",
        "chalk on pavement",
    ],
    "screen and machine": [
        "LED dot matrix", "old CRT screen", "thermal receipt printer", "brutalist web page",
        "early 3D video game", "phone screenshot", "spreadsheet chart", "vector icon set",
        "glitched video frame", "airport departure board", "arcade cabinet art", "e-ink display",
        "low poly render", "CAD wireframe", "pixel font on a car dashboard",
    ],
    "camera and science": [
        "flash film photo", "long exposure photo", "infrared photo", "x-ray image",
        "thermal camera image", "satellite image", "microscope image", "security camera still",
        "night vision footage", "macro photo", "drone photo from straight above", "sonar scan",
        "weather radar map", "motion blur photo", "underwater photo",
    ],
    "material and light": [
        "neon tubes", "stained glass", "mosaic tiles", "glazed ceramic", "glossy 3D render",
        "chrome and glass render", "holographic foil", "clay model photo", "inflatable plastic",
        "folded paper", "string and pins", "carved wood relief", "light painting",
        "shadow puppets", "frosted acrylic with backlight",
    ],
}

VISUAL = {
    "color": [
        "one ink only", "black and white with one accent", "two colors that clash",
        "colors taken from the subject's material", "full color with one hue in charge",
        "very pale and high key", "very dark and low key", "fluorescent", "only earth colors",
        "metallic", "colors of a place at a set hour", "gray with one warm spot",
        "cold colors only", "warm colors only", "the colors of a machine screen", "colors of food",
        "colors of a bruise", "two near colors and one far one", "colors of cheap plastic",
        "rust and oxidized metal", "colors of a fruit going bad", "pastel with one harsh dark",
        "primary colors and nothing else", "colors of a hospital corridor",
        "all one hue from darkest to lightest", "colors of dust and concrete",
        "colors of a supermarket aisle", "colors of a swimming pool", "colors of sunburn and shadow",
        "colors of a bus route map",
    ],
    "layout": [
        "subject huge and cropped by the edges", "subject tiny in a large empty field",
        "seen from straight above", "seen from far below", "one detail very close",
        "one thing repeated many times", "split into two halves", "the text is the image",
        "strong diagonal", "low and off center", "deep layers from front to back",
        "a crowd of small parts", "a single line across the frame", "framed by something in front",
        "upside down or turned", "one big shape and nothing else",
        "a grid with one cell broken", "a tall strip with empty sides", "a ring around an empty center",
        "a staircase of steps", "overlapping see-through sheets", "a column pressed to one edge",
        "the horizon at the very top", "scattered from corner to corner", "many small panels",
        "everything pushed into one corner", "a spiral from the center out", "a frame inside a frame",
        "a tight band across the middle", "one part sliced and shifted",
    ],
    "type": [
        "hand lettered", "cut out letters", "stencil letters", "tall condensed", "very wide",
        "old style serif", "typewriter", "flowing script", "stacked words", "type on a curve",
        "only small type", "one giant word", "letters built from the subject", "mixed found letters",
        "no type at all if allowed", "type set vertically",
        "pixel letters", "heavy slab serif", "thin even-stroke sans", "round bubble letters",
        "blackletter", "letters of different sizes in one word", "outlined letters with no fill",
        "letters with an offset shadow", "numbers instead of words", "letters partly rubbed away",
        "letters spaced very far apart", "small lowercase sans", "handwriting on a form",
        "letters cut from a grid of dots",
    ],
}

TEXT = {
    "voice": [
        "a witness in first person", "instructions in second person", "a plain list",
        "a short letter", "overheard dialogue", "one long sentence", "short fragments",
        "question and answer", "a note left for someone", "a review by someone tired",
        "a child explaining it", "someone who disagrees", "a voice from the future looking back",
        "a rumor passed on",
    ],
    "entry": [
        "a sound", "a smell", "a single object", "a mistake", "a rule", "a place",
        "the ending", "a body feeling", "a thing that is missing", "a complaint", "a habit",
        "a misunderstanding", "a gesture", "a question nobody answers",
    ],
    "register": [
        "plain", "formal", "dry", "warm", "blunt", "playful", "terse", "careful", "nervous", "proud",
    ],
}

IDEA = {
    "verb": [
        "trade", "hide", "build", "repair", "sort", "follow", "trap", "grow", "deliver", "swap",
        "borrow", "steal", "listen", "stack", "balance", "burn", "wash", "guess", "herd", "queue",
        "bargain", "cook", "dig", "signal", "wait", "measure", "lose", "rescue", "copy", "share",
    ],
    "constraint": [
        "only one try", "it gets worse when you wait", "you cannot see it directly",
        "someone else controls half of it", "all of it is borrowed and must go back",
        "it only works in one place", "two rules that fight", "the tool wears out with use",
        "the crowd decides", "you are too small for it", "nobody speaks the same language",
        "the reward is also the cost", "it must be done in silence", "it happens to many at once",
    ],
    "scale": [
        "one person", "a family", "a street", "a whole town", "a crowd of strangers",
        "a machine", "an animal", "a single room", "two rivals", "a team that does not get along",
        "a queue", "a night shift", "a class of children", "a flock", "a whole building",
        "a couple", "a village on one road", "one market stall", "one object passed from hand to hand",
        "a swarm", "a vehicle and its passengers", "a choir", "a household of strangers",
        "one hour", "a whole country", "old friends", "a one-person business", "a block of flats",
        "two siblings", "a waiting room",
    ],
    "pressure": [
        "a deadline", "a rival", "a debt", "weather", "a rule that changes", "noise", "hunger",
        "a promise", "a rumor", "running out of space", "a guest who will not leave", "fatigue",
    ],
}

ANCHOR = [
    "ladder", "bicycle", "glove", "mirror", "bread", "magnet", "compass", "hinge", "fog", "bee",
    "copper", "thread", "lamp", "drum", "sponge", "scissors", "ice", "cactus", "radio", "bridge",
    "key", "feather", "brick", "orange", "train", "coin", "bone", "cloud", "button", "mushroom",
    "wire", "fan", "tooth", "bell", "window", "kite", "ash", "honey", "nail", "moth", "paint",
    "tent", "elevator", "umbrella", "cassette", "dice", "spoon", "candle", "lock", "stairs",
    "battery", "garden hose", "skateboard", "laundry", "traffic cone", "ticket", "alarm clock",
    "snail", "cable", "balloon", "ring", "knot", "crane", "pump", "mask", "barcode", "tire",
    "zip", "comb", "fork", "parachute", "chair", "puddle", "smoke", "chili", "rice", "sand",
    "escalator", "satellite dish", "lemon", "goat", "camel", "bamboo", "lantern", "scooter",
    "vending machine", "pigeon", "ceiling fan", "water tank", "mango", "plastic chair", "antenna",
    "glass bottle", "sunflower", "cardboard box", "headphones", "rug", "tea glass", "bus",
]

SETTING = [
    "a rooftop", "a parking lot after closing", "a highway service station", "a night bus",
    "a housing block courtyard", "a shopping mall basement", "the industrial edge of town",
    "a stadium after the match", "a train station", "a border crossing", "a student dorm",
    "a market in the rain", "a neighborhood still being built", "an airport at night",
    "a car wash", "a laundromat", "a wedding", "a server room", "a hospital corridor",
    "a school gym", "a gas station far from town", "a food court", "a construction crane cab",
    "a bus depot", "a hotel kitchen", "a police station waiting room", "a hair salon",
    "a local radio station", "a cemetery on a holiday", "a car repair shop", "a back yard",
    "a supermarket at closing time", "an apartment stairwell", "a power plant", "a funeral",
    "a playground at dusk", "a public pool", "a post office", "a phone repair stall",
    "the open land outside town", "the highest place nearby", "the water nearest the town",
]

REGION = [
    "Georgia (the country)", "northern Chile", "Kerala", "Hokkaido", "the Scottish Highlands",
    "Anatolia", "Sicily", "Ghana", "Mongolia", "Quebec", "Java", "the Faroe Islands", "Oaxaca",
    "Morocco", "Finnish Lapland", "the Philippines", "Patagonia", "Kenya", "Vietnam", "Iceland",
    "Bavaria", "Poland", "Sri Lanka", "the Andes of Peru", "Portugal", "Nigeria", "Korea",
    "Brazil's northeast", "Ukraine", "Ethiopia", "Wales", "Nepal", "Senegal", "Sardinia",
    "Kazakhstan", "the Basque Country", "Tasmania", "Cuba", "Bangladesh", "the American Midwest",
    "Iran", "Croatia", "Colombia", "Taiwan", "Egypt", "Norway", "Bolivia", "Uzbekistan",
]
NO_ANCHOR = [
    "no single object, build it from a pattern of the place",
    "no single object, only type",
    "no single object, a crowd of people",
    "no single object, numbers or data from the subject",
    "no single object, a field of light or color",
    "no single object, the surface of the place up close",
]

FIXED_COLOR = {
    "x-ray image", "thermal camera image", "night vision footage", "infrared photo", "sonar scan",
    "weather radar map", "e-ink display", "thermal receipt printer", "photocopy zine",
    "LED dot matrix", "airport departure board", "security camera still",
}
CLASH = [
    ({"layout": "the text is the image"}, {"type": "no type at all if allowed"}),
    ({"layout": "the text is the image"}, {"type": "only small type"}),
    ({"anchor": "no single object, only type"}, {"type": "no type at all if allowed"}),
    ({"type": "one giant word"}, {"layout": "subject tiny in a large empty field"}),
]

HAND_METHODS = {
    "woodcut", "screen print", "rubber stamp", "spray stencil", "cut paper collage", "gouache",
    "ink brush", "ballpoint sketch", "marker on cardboard", "embroidery", "hand painted shop sign",
    "children's crayon drawing", "spray paint graffiti", "chalk on pavement",
}
MACHINE_METHODS = {
    "LED dot matrix", "old CRT screen", "thermal receipt printer", "early 3D video game",
    "phone screenshot", "spreadsheet chart", "vector icon set", "airport departure board",
    "e-ink display", "low poly render", "CAD wireframe", "pixel font on a car dashboard",
}
HAND_TYPES = {"hand lettered", "cut out letters", "flowing script", "handwriting on a form", "round bubble letters"}
MACHINE_TYPES = {"pixel letters", "typewriter", "letters cut from a grid of dots"}


def family_of(m):
    for family, items in METHOD_FAMILIES.items():
        if m in items:
            return family
    return None


def method():
    family = rng.choice(list(METHOD_FAMILIES))
    return pick("method", METHOD_FAMILIES[family])


def clashes(seed):
    for a, b in CLASH:
        if all(seed.get(k) == v for k, v in a.items()) and all(seed.get(k) == v for k, v in b.items()):
            return True
    m = seed.get("method")
    if m is None:
        return False
    t = seed.get("type")
    if (m in MACHINE_METHODS and t in HAND_TYPES) or (m in HAND_METHODS and t in MACHINE_TYPES):
        return True
    if m in FIXED_COLOR:
        return seed.get("color") != "the method's own colors"
    if seed.get("color") == "the method's own colors":
        return True
    return seed.get("color") == "the colors of a machine screen" and family_of(m) != "screen and machine"


def pools(kind):
    if kind == "visual":
        return {"method": None, **VISUAL}
    if kind == "text":
        return dict(TEXT)
    return dict(IDEA)


def roll_once(kind, keep, only=None):
    out = {}
    for name, items in pools(kind).items():
        out[name] = method() if items is None else pick(name, items)
    if kind == "visual":
        out["verb"] = pick("verb", IDEA["verb"])
        out["scale"] = pick("scale", IDEA["scale"])
    out["setting"] = pick("setting", SETTING)
    out["region"] = pick("region", REGION)
    if kind == "visual" and rng.random() < 0.5:
        out["anchor"] = pick("anchor", NO_ANCHOR)
    else:
        out["anchor"] = pick("anchor", ANCHOR)
    out.update(keep)
    if only:
        out = {k: v for k, v in out.items() if k in keep or k == only}
    if out.get("method") in FIXED_COLOR and "color" in out and "color" not in keep:
        out["color"] = "the method's own colors"
    return out


def axes_of(kind):
    return list(roll_once(kind, {}))


def allowed(kind):
    values = {}
    for name, items in pools(kind).items():
        values[name] = [m for family in METHOD_FAMILIES.values() for m in family] if items is None else list(items)
    if kind == "visual":
        values["color"].append("the method's own colors")
        values["verb"] = list(IDEA["verb"])
        values["scale"] = list(IDEA["scale"])
    values["setting"] = list(SETTING)
    values["region"] = list(REGION)
    values["anchor"] = ANCHOR + (NO_ANCHOR if kind == "visual" else [])
    return values


def roll(kind, keep=None, only=None):
    keep = keep or {}
    for _ in range(200):
        seed = roll_once(kind, keep, only)
        if not clashes(seed):
            return seed
    sys.exit("the kept axes clash with each other; keep fewer")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", nargs="?", default="visual", choices=["visual", "text", "idea"])
    ap.add_argument("--only", help="roll one axis again, for example --only method")
    ap.add_argument("--keep", action="append", default=[], help="an axis you keep, for example --keep \"method=x-ray image\"")
    ap.add_argument("--no-log", action="store_true", help="do not save this seed to the history")
    args = ap.parse_args()
    load_recent(args.kind)
    keep = {}
    for item in args.keep:
        k, sep, v = item.partition("=")
        if not sep:
            sys.exit(f"--keep needs axis=value, got '{item}'")
        keep[k.strip()] = v.strip()
    axes = axes_of(args.kind)
    for name in [*keep, *([args.only] if args.only else [])]:
        if name not in axes:
            sys.exit(f"no axis '{name}' for {args.kind}; axes: {', '.join(axes)}")
    valid = allowed(args.kind)
    for name, value in keep.items():
        if value not in valid[name]:
            sys.exit(f"'{value}' is not a value of axis '{name}'; values: {'; '.join(valid[name])}")
    if args.only:
        keep.pop(args.only, None)
    seed = roll(args.kind, keep, args.only)
    if args.only:
        seed = {args.only: seed[args.only]}
    for k, v in seed.items():
        print(f"{k}: {v}")
    if not args.no_log and not args.only:
        history.add({"type": "seed", "kind": args.kind, "seed": seed})


if __name__ == "__main__":
    main()

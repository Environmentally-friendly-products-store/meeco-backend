def cyrillic_slug_maker(string):
    symbols = (
        "абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
        (
            *list("abvgdee"),
            "zh",
            *list("zijklmnoprstuf"),
            "kh",
            "z",
            "ch",
            "sh",
            "sh",
            "",
            "y",
            "",
            "e",
            "yu",
            "ya",
            *list("ABVGDEE"),
            "ZH",
            *list("ZIJKLMNOPRSTUF"),
            "KH",
            "Z",
            "CH",
            "SH",
            "SH",
            *list("_Y_E"),
            "YU",
            "YA",
            "_",
        ),
    )

    coding_dict = dict(zip(*symbols))
    fin = []
    for item in string:
        fin.append(coding_dict.get(item, item))
    return "".join(fin)

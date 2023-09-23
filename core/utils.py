def cyrrilic_slugmaker(string):
    symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ ",
        (*list(u'abvgdee'), 'zh', *list(u'zijklmnoprstuf'), 'kh', 'z', 'ch', 'sh', 'sh', '',
        'y', '', 'e', 'yu','ya', *list(u'ABVGDEE'), 'ZH', 
        *list(u'ZIJKLMNOPRSTUF'), 'KH', 'Z', 'CH', 'SH', 'SH', *list(u'_Y_E'), 'YU', 'YA', '_'))

    coding_dict = {source: dest for source, dest in zip(*symbols)}
    fin = []
    for item in string:
        fin.append(coding_dict.get(item, item))
    return ''.join(fin)

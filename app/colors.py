from colorsys import rgb_to_hls
from math import fabs

color_palette = {
    'white': 0xFFFFFF,
    'grey': 0x888888,
    'black': 0x000000,
    'red': 0xFF0000,
    'green': 0x00FF00,
    'blue': 0x0000FF,
    'darkgreen': 0x006600,
    'darkblue': 0x000066,
    'orange': 0xFF8000,
    'cyan': 0x00FFFF,
    'magenta': 0xFF00FF,
    'yellow': 0xFFFF00
}
color_palette_invert = { value: key for key, value in color_palette.items() }

def rgb_to_web(rgb):
    return "#{:0>6}".format(hex(rgb)[2:].upper())

def rgb_tuple(rgb_value, as_float=True):
    int_tuple = (
            (rgb_value & 0xFF0000) >> 16,
            (rgb_value & 0x00FF00) >> 8,
            rgb_value & 0x0000FF
            )
    if as_float:
        return tuple([x/256.0 for x in int_tuple])
    return int_tuple

color_palette_hls = { key: rgb_to_hls(*rgb_tuple(value)) for key, value in color_palette.items() }


def nearest(rgb, color_palette_hls=color_palette_hls):
    def __hls_tuple_coefficient(first, second):
        return sum([fabs(first[idx]-second[idx]) for idx in range(3)])
    def __color_info(name):
        return {'name': name, 'rgb': color_palette[name], 'web': rgb_to_web(color_palette[name])}

    nrst = {
        'color': {
            'name': None,
            'rgb': None,
            'web': None,
            },
        'coeff': 3.0,
        }

    h, l, s = rgb_to_hls(*rgb_tuple(rgb))

    if 'black' in color_palette and l < 0.125:
        nrst['color'] = __color_info('black')
        return nrst
    if 'white' in color_palette and l > 0.875:
        nrst['color'] = __color_info('white')
        return nrst
    if 'grey' in color_palette and s < 0.125:
        nrst['color'] = __color_info('grey')
        return nrst

    for key, value in color_palette_hls.items():
        current_coeff = __hls_tuple_coefficient(value, (h, l, s))
        if current_coeff < nrst['coeff']:
            nrst['coeff'] = current_coeff
            nrst['color']['name'] = key

    nrst['color'] = __color_info(nrst['color']['name'])

    return nrst


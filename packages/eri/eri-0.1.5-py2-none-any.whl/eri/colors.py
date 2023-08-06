#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Module: colors.py
Author: zlamberty
Created: 2018-08-22

Description:
    official eri company colors as defined in the brand and style guide

Usage:
    import eri.colors

"""

import collections

EriColor = collections.namedtuple(
    'EriColor',
    ['name', 'rgb', 'cmyk', 'hex']
)

DARK_BLUE = EriColor(
    'Dark Blue',
    (0, 45, 115),
    (100, 88, 27, 19),
    '#002D73',
)
LIGHT_BLUE = EriColor(
    'Light Blue',
    (64, 124, 202),
    (75, 45, 0, 0),
    '#407CCA',
)
CORONA_RED = EriColor(
    'Corona Red',
    (226, 35, 26),
    (5, 98, 100, 0),
    '#E2231A',
)
CORONA_YELLOW = EriColor(
    'Corona Yellow',
    (255, 197, 1),
    (0, 23, 100, 0),
    '#FFC501',
)
WHITE = EriColor(
    'White',
    (255, 255, 255),
    (0, 0, 0, 0),
    '#FFFFFF',
)
BLACK = EriColor(
    'Black',
    (0, 0, 0),
    (0, 0, 0, 100),
    '#000000',
)

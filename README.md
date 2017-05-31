# SvgLayerParser
python module for parsing a .svg file produced from slic3r --extract-svg and outputting an xml string with a given number of layers

usage:

import SvgParser

filename = "/homes/..../foo.svg"
layers = build(filename, 42)

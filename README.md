# SvgLayerParser
python module for parsing a .svg file produced from slic3r --extract-svg and outputting an xml string with a given number of layers


First ensure you are in Slic3r directory or you have the environment variable SLIC3R_HOME s.a 

SLIC3R_HOME=/home/user/slic3r/    for *nix

set SLIC3R_HOME=c:\slic3r\        for win

usage:

import SvgParser

SvgParser.init(filename)


or use as a script:

python SvgParser.py 3dobject.stl 

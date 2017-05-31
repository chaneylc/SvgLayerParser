# SvgLayerParser
python module for parsing a .svg file produced from slic3r --extract-svg and outputting an xml string with a given number of layers

usage:

import SvgParser

filename = "/homes/..../foo.svg"
layers = build(filename, 42)


example output:

<?xml version="1.0" encoding="UTF-8" standalone="yes"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd"><svg xmlns="http://www.w3.org/2000/svg" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:slic3r="http://slic3r.org/namespaces/slic3r" width="188.292129" height="132.216156">
  <g xmlns="http://www.w3.org/2000/svg" xmlns:slic3r="http://slic3r.org/namespaces/slic3r" xmlns:svg="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" id="layer0" slic3r:z="1.75e-007">   ..... <g .... id="layer42">..... </svg>

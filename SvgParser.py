from lxml import etree

#namespaces
z = '{http://slic3r.org/namespaces/slic3r}z' #namespace for z layer in attributes
g = '{http://www.w3.org/2000/svg}g'          #namespace for g tag in svg element
svg = '{http://www.w3.org/2000/svg}svg'      #namespace for svg tag in root 

def build(filename, numLayers):
    
    #need this header line for correctly formatted svg file
    header = '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'
    
    layers = [] #list of elements (g) to create svg from
    tree = etree.parse(filename)
    for elem in tree.getiterator():
        if svg in elem.tag: #found svg header
            header += etree.tostring(elem).split("<g")[0]
        if g in elem.tag: #found layer
            layer = elem.attrib.get('id')
            if int(layer.split("layer")[1]) <= numLayers:
                layers.append(etree.tostring(elem).replace('\n', ''))
            else : 
                break
    return header + "".join(layers) + "</svg>" 



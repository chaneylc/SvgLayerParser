#!/usr/bin/env python

from subprocess import Popen, PIPE
from lxml import etree
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import os

SLIC3R_HOME=None
if "SLIC3R_HOME" in os.environ:
    SLIC3R_HOME = os.environ["SLIC3R_HOME"]
else : 
    SLIC3R_HOME = os.getcwd()  
SLIC3R_SCRIPT = os.path.join(SLIC3R_HOME, "slic3r.pl")
print("Slic3r home: {}".format(SLIC3R_HOME))
print("Slic3r script: {}".format(SLIC3R_SCRIPT))



#function takes .svg filename as input and number of layers to be built
#used slic3r.pl --export-svg as reference .svg
def build(filename, numLayers):

    #namespaces
    z = '{http://slic3r.org/namespaces/slic3r}z' #namespace for z layer in attributes
    g = '{http://www.w3.org/2000/svg}g'          #namespace for g tag in svg element
    svg = '{http://www.w3.org/2000/svg}svg'      #namespace for svg tag in root 
    
    #need this header line for correctly formatted svg file
    header = '''<?xml version="1.0" encoding="UTF-8" standalone="yes"?>
                <!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" 
                "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">'''.replace('\n', '')
    
    layers = [] #list of elements (g) to create svg from
    tree = etree.parse(filename)

    for elem in tree.getiterator():

        if not elem.tag is etree.Comment:
            if svg in elem.tag: #found svg header
                header += etree.tostring(elem).split("<g")[0]
            if g in elem.tag: #found layer
                layer = elem.attrib.get('id')
                if int(layer.split("layer")[1]) <= numLayers:
                    layers.append(etree.tostring(elem).replace('\n', ''))
                else : 
                    break
    return header + "".join(layers) + "</svg>" 

def createIdeal(layer, filePrefix):

    #valid svg file string
    rawString = build("{}.svg".format(filePrefix), layer)
    #create temp .svg and write rawstring to file
    f = open("tempSvg.svg", 'w')
    f.write(rawString)
    f.close()
    #use svg2rlg lib to create .png
    drawing = svg2rlg("tempSvg.svg")
    #ideal files will be named e.g bikiniIdeal_1.png for layer 1
    renderPM.drawToFile(drawing, "{}Ideal_{}.png".format(filePrefix, layer))

#implement camera object capture 
def captureActual(layer):

    #filename should be "{}Actual_{}.png" s.a: bikiniActual_1.png for layer 1
    pass

#utilize printrun library to call this list of commands
def printCode(code):

    commandString = "".join(code)
    #use printrun lib to call must be a blocking command

#our image analysis algorithm goes here
def analyzeActualAndIdeal(layer, filePrefix):
   
    ideal = "{}Ideal_{}.png".format(filePrefix, layer)
    actual = "{}Actual_{}.png".format(filePrefix, layer)
    if os.path.isfile(ideal) and os.path.isfile(actual):
        try:
            idealImg = open(ideal, 'r')
            actualimg = open(actual, 'r')
            
            #image analysis code

            idealImg.close()
            actualImg.close()
        except Exception as e:
            print e


#the main function to run the experiment
def run(filePrefix):

    #initialize filenames and check if they exist before continuing
    gcodeFilename = filePrefix + ".gcode"
    svgFilename = filePrefix + ".svg"
    if os.path.isfile(gcodeFilename) and os.path.isfile(svgFilename):
        try :
            #load .gcode string into a list
            gcode = open(gcodeFilename).readlines()
            #layerCode holds the commands for a single layer
            layerCode = [] 
            #foreach line add the code to our list
            #check if it calls the 'next layer' identifier
            #if it does, print the layer and capture actual image
            #create png to compare with actual
            for line, code in enumerate(gcode):
                layerCode.append(code)
                if "; move to next layer" in code:
                   #print layerCode
                   layer = int(code.split('(')[1].split(')')[0])
                   #this call blocks until print layer is complete
                   printCode(layerCode)
                   #skip cam check for code before first layer
                   if not layer == 0: #and len(layerCode) >= 5 ?
                       #print "attempting capture"
                       captureActual(layer)
                       #print "attempting create ideal"
                       createIdeal(layer, filePrefix) 
                       #print "attempting analyze"
                       analyzeActualAndIdeal(layer, filePrefix)

                   #reset layer code
                   layerCode = []

        except Exception as e:
            print gcodeFilename, svgFilename
            print e


#the function to create .gcode and .svg
#user gives a 3d object file and kwargs for passing directly to 
#slic3r when executing gcode --not-implemented yet--
def init(fileStl=None, isRun=True, **kwargs):
    
    if fileStl:
        cwd = os.getcwd()
        absFileStl = os.path.join(cwd, fileStl)
        #grab the file prefix to write .gcode and .svg file
        filePrefix = os.path.join(cwd, fileStl.split('.')[0])
        try :
            #call slic3r to create gcode
            p = Popen('perl {} --gcode-comments -o {}.gcode {}'\
                    .format(SLIC3R_SCRIPT, filePrefix, absFileStl))
            p.wait()
            p.terminate()
            p.kill()
            #call slic3r to create svg
            p = Popen('perl {} --export-svg -o {}.svg {}'\
                    .format(SLIC3R_SCRIPT, filePrefix, absFileStl))
            p.wait()
            p.terminate()
            p.kill()

            if isRun:
                run(filePrefix)

        except Exception as e:
            print e

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print "Running in script mode: {}".format(sys.argv[0])
        print "Executing on 3d object: {}".format(sys.argv[1])
        inputFilename = sys.argv[1]
        if os.path.isfile(inputFilename):
            init(inputFilename)
        else: #check if they gave relative path
            absFilename = os.path.join(os.getcwd(), inputFilename)
            if os.path.isfile(absFilename):
              init(absFilename)

#!/usr/bin/python
#
# convert 0.3.5 modules to 0.4
#
# syntax:
#
# convert.py moduleid
#

import os, sys, re, string, commands, exceptions


class ConvertError(exceptions.Exception):
    def __init__(self, args=None):
        self.args = args


def removeAttribute(tag, attribute, text):

    pattern = re.compile("(<%s[^>]*)%s\s*=\s*['\"]([^'\"]*)['\"]([^>]*>)" % (tag, attribute))
    result = pattern.search(text, re.DOTALL)
    text = pattern.sub(r"\1\3", text)

    return (result.group(2), text)


def doConvert(text):

    # Replace all occurances of 0.3.5 with 0.4
    pattern = re.compile(r"0\.3\.5")
    text = pattern.sub("0.4", text)

    # Match key parts of the <module> tag.  These could come in any order
    (version, text) = removeAttribute('module', 'version', text)
    (created, text) = removeAttribute('module', 'created', text)
    (revised, text) = removeAttribute('module', 'revised', text)
    (levelmask, text) = removeAttribute('module', 'levelmask', text)

    # Pull out metadata section
    metadataPattern = re.compile(r"(<metadata>\s*)(.*)(\s*</metadata>)", re.DOTALL)
    metadata = metadataPattern.search(text).group(2)
    
    # Put metadata namespace prefix on metadata tags
    metadata = re.sub("<(/?)([^>]*)>", "<\g<1>md:\g<2>>", metadata)

    # Add new metadata tags
    metadata = """
    <md:version>%s</md:version>
    <md:created>%s</md:created>
    <md:revised>%s</md:revised>
""" % (version, created, revised) + metadata

    # Replace metadata section
    text = metadataPattern.sub(r"\1%s\3" % metadata, text)
    
    return text


def convertFiles(files):
    
    for filename in files:
        print "Converting %s" % filename
        # Read data from file
        fileIn = open(filename,'r')
        dataIn = fileIn.read()
        fileIn.close()

        # Do actual conversion
        try:
            dataOut = doConvert(dataIn)
        except ConvertError, e:
            print "ERROR: %s" % e
            sys.exit(-1)

        # Write data back to file
        if (dataOut):
            fileOut = open(filename, 'w')
            fileOut.write(dataOut)
            fileOut.close()
  
        # Perform vlidation check
        output = commands.getoutput('rxp -xVs %s' % filename)
        if output:
            print "ERROR: validation failed: %s" % output


if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print "Usage: convert.py FILE1 [FILE2] ..."
        sys.exit(-1);

    convertFiles(sys.argv[1:])




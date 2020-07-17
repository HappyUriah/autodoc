#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys
import os
import delstarComment as starComment
import delMacro as macro

mediaFile = "starComment.h"

if os.path.exists(mediaFile):
    os.remove(mediaFile)

intput = sys.argv[1] + ""
print(type(input))

starComment.rmStarComment(sys.argv[1], mediaFile)
input = mediaFile
output = "output.md"
macro.rmMacroAndAnsis(mediaFile, output)
os.remove(mediaFile)



       





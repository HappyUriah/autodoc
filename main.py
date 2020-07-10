#!/usr/bin/python
# -*- coding: UTF-8 -*-

import sys
import enumParse as enum
import structParse as struct
import funcParse as func

def isStruct(block):
    for line in block :
        if ' struct ' in line or line.strip().startswith("struct "):
            return True
    return False

def isEnum(block):
    for line in block :
        if ' enum ' in line or line.strip().startswith("enum "):
            return True
    return False



def isFunc(block) : 
    body = ""
    for line in block :
        if not func.isComment(line) and not func.isHaskKey(line) :
            body += line

    
    if "(" in body and ")" in body :
        return True
    return False


  

fout = open('output.md','a+')



f = open(sys.argv[1])               # 返回一个文件对象 
line = f.readline()               # 调用文件的 readline()方法 
block = []
remain = True
while line:
    #print(len(line))
    line = line.strip()
    if line : 
        remain = True;
        block.append(line)
    else :
        remain = False;
    
    
    if remain == False and len(block) > 0  :
        #print(block)
        #print('\n\n\n')

        if isEnum(block) :
            enum.ansisEnumBlock(block,fout)
            print('\n\n\n')
        elif isStruct(block) :
            struct.ansisStructBlock(block, fout)
            print('\n\n\n')
        elif isFunc(block) :
            func.ansisFunctionBlock(block, fout)
            print('\n\n\n')
        block.clear()



    line = f.readline() 
 
f.close()
fout.close()


#!/usr/bin/python
# -*- coding: UTF-8 -*-

def containsKeyWord(strs):
    keyword =("enum","struct","class", "typedef")
    eles = strs.split()
    for ele in eles:
        if ele in keyword:
            return True
    
    return False

def valid(strs, blocks):
    if strs.count(',') > 0 :
        print("wrong format!!!!,请注意换行")
        return False

    found = False
    for line in blocks:
        if "///<" in line:
            found = True
            break
    return found
    # elif strs.find("///<") == -1 :
    #     print("请添加注释")
    #     return False
    # return True
    

def ansisOtherBlock(strs, blocks):

    if containsKeyWord(strs):
        print("声明语句")
    else :
        assert valid(strs, blocks)


    
    
    
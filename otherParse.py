#!/usr/bin/python
# -*- coding: UTF-8 -*-
import common as comm

def containsKeyWord(strs):
    keyword =("enum","struct","class", "typedef")
    eles = strs.split()
    for ele in eles:
        if ele in keyword:
            return True
    
    return False

def valid(strs, blocks):
    if strs.count(',') > 0 :
        print("\033[31m%s" % strs + "请注意换行")
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

def extractComment(blocks):
    keyword = "///<"
    for line in blocks:
        if keyword in line:
            desc = line[line.find(keyword) + len(keyword) :].strip()
            return desc
    return None

# 解析变量名
def parseVarName(strs) :
    items = strs.split();
    num = len(items)
    
    name=""
    if items[-1] == ";":
        name = items[-2]
    else :
        name = items[-1][:-1]
    
    if "[" in name :
        name = name[:name.find('[')]

    return name

def writeVarToFile(varName, comment,  fout):
    fout.write('## ' + varName + '\n\n')
    fout.write('*说明*\n\n')
    fout.write(comment)
    
    fout.write('\n\n')
    

def ansisOtherBlock(strs, blocks, fout, classname=None):

    if containsKeyWord(strs):
        print("声明语句")
    else :
        comm.assertStr(valid(strs, blocks), " 缺少注释")
        name = parseVarName(strs)

        if classname:
            name = classname + "::" + name
        print("变量名称为", name)
        comm.assertStr(name, " 变量名不能为空")
        desc = extractComment(blocks)

        comm.assertStr(desc, " 变量缺少注释")
        writeVarToFile(name, desc, fout)
        

    
    
    
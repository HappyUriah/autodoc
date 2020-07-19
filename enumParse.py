#!/usr/bin/python
# -*- coding: UTF-8 -*-

import common as comm

def isEnum(strs):
    eles = strs.split()
    print(eles)

    if len(eles) < 3:
        return False
    
    if eles[0] == "enum":
        return True
    if eles[0] == "typedef" and eles[1] == "enum" :
        return True
    return False



#提取描述信息
def extractBrief(blocks) :
    word="\\brief "
    brief = ""
    start = -1
    num = len(blocks)
    for id in range(0, num):
        line = blocks[id].strip()
        if word in line :
            start = id + 1
            brief += line[line.find(word) + len(word):]
        elif id == start and   line.startswith("//") :
            start +=1
            brief += line.strip('/')

    #print("brief = " , brief)
    return brief

#解析枚举名称
def extractName(strs) :
    eles = strs.split()
    if eles[0] == "enum" and eles[1] == "class" :
        return eles[2].strip('{};')
    elif eles[0] == "enum":
        return eles[1].strip('{};')
    elif eles[0] == "typedef" and eles[-1] == ';' :
        return eles[-2].strip('{};')
    else :
        return eles[-1][:-1].strip('{};')

# 校验合法性，主要判断是否存在多行项
def valid(blocks) :
    for line in blocks:
        line = line.strip()
        if line.startswith("//"):
            continue
        else :
            line = comm.rmComment(line).strip()
            if line.count(",") + line.count("{") + line.count("}") > 1:
                print("wrong format!!!!,请注意换行")
                return False
            elif line.count(",") == 1 and not line.endswith(","):
                print("wrong format!!!!,请注意换行")
                return False
          
    
    return True




def extractEnumEle(blocks) :

    start = -1
    end = -1
    num = len(blocks)
    for i in range(0,num):
        line = blocks[i].strip()
        if line.startswith("//"):
            continue
        else :
            #print(line)
            line = comm.rmComment(line)
            #print(line)
            if "{" in line:
                start = i
                #print("start = ", start)
            elif "}" in line:
                end = i
    #print("start = ", start)
    #print("end = ", end)
    
    
    assert start != -1
    assert end != -1
    assert start < end

    keyword = '///<'
    items = []
    for i in range(start + 1, end):
        line = blocks[i].strip()
        if not line or line.startswith("//"):
           continue

        comm.assertStr(line.find(keyword) != -1, line +"需要注释")
        des = line[line.find(keyword) + len(keyword): ]
        comm.assertStr(des, line + "需要注释")
        line = comm.rmComment(line)
        strs = line.split()

        #print(strs)
        comm.assertStr(len(strs) > 2, "枚举项格式为 *a = 1 ///< a*")
        
        key = strs[0];
        value = strs[2].strip(',')
        kvd=(key,value, des)
        items.append(kvd)

    return items


    
def writeEnumToFile(brief, name, items, f) :
    f.write('\n\n### ' + name + '\n')
    f.write('*枚举描述*\n\n')
    f.write(brief + '\n\n')
    f.write("|枚举名      |    枚举值 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    #cnt = len(ele)
    for item in items:
        f.write("|" + item[0] + "|" + item[1] + "|" + item[2] + "|\n")
  




def ansisEnumBlock(strs, blocks, fout, classname=None):

    name = extractName(strs).strip()
    print("name = ", name);
    comm.assertStr(name, "枚举名不能为空")
    #assert name

    brief = extractBrief(blocks)
    print("brief = ", brief)
    comm.assertStr(brief, "枚举描述不能为空")
    #assert brief


    assert valid(blocks)

    items = extractEnumEle(blocks)
    print("enum items = ", items);

    writeEnumToFile(brief, name, items, fout)
    
#!/usr/bin/python
# -*- coding: UTF-8 -*-
import common as comm

import common as comm

def isStruct(strs):
    eles = strs.split()
    print(eles)

    if len(eles) < 3:
        return False
    
    if eles[0] == "struct":
        return True
    if eles[0] == "typedef" and eles[1] == "struct" :
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


#解析结构体名称
def extractName(strs) :
    eles = strs.split()
    if eles[0] == "struct":
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
            if line.count("{") + line.count(";") > 1:
                print("wrong format!!!!,请注意换行")
                return False
            elif line.find(";") != -1 and line.find("}") != -1 and  line.find(";") < line.find("}"):
                print("wrong format!!!!,请注意换行")
                return False
         
          
    
    return True

def extractArrayEle(note) :
    strs = note.split()

    for str1 in strs:
        if('[' in str1) :
            val = str1[:str1.find('[')]
            break
    typ = note[0: note.find(val)]
    typ += '[]'
    return typ, val

def extractValEle(note) :
    strs = note.split()
    num = len(strs)
    
    lastStr = strs[num - 1]
    if lastStr == ";" :
        assert num > 2 
        val = strs[num - 2]
    else :
        val = lastStr[0:-1]
    typ = note[0: note.find(val)]
    return typ, val
    


def extractStructEle(blocks) :

    start = -1
    end = -1
    num = len(blocks)
    for i in range(0,num):
        line = blocks[i].strip()
        if line.startswith("//"):
            continue
        else :
            line = comm.rmComment(line)
            if "{" in line:
                start = i
             
            elif "}" in line:
                end = i
   
    
    assert start != -1
    assert end != -1
    assert start < end

    keyword = '///<'
    items = []
    for i in range(start + 1, end):
        line = blocks[i].strip()
        if  line == "" :
            continue
        elif line.startswith("//"):
            continue
        
      #  print("#############", line)
        assert line.find(keyword) != -1
        des = line[line.find(keyword) + len(keyword): ]
        assert des
        note = comm.rmComment(line)
       
        if '[' in note :
            # 数组
            typ, val = extractArrayEle(note)
            tvd = (typ, val, des)
            items.append(tvd)
        else :
            typ, val = extractValEle(note)
            tvd= (typ, val, des)
            items.append(tvd)


    return items

def writeStructToFile(brief, name, items, f) :
    f.write('\n\n### ' + name + '\n\n')
    f.write('*结构体描述*\n\n')
    f.write(brief + '\n\n')
    f.write("| 类型      |    变量 | 描述  |\n| :-------- | --------:| :--: |\n")
   
    
    for item in items:
        f.write("|" + item[0] + "|" + item[1] + "|" + item[2] + "|\n")


def ansisStructBlock(strs, blocks, fout, classname=None):
    name = extractName(strs).strip()
    print("name = ", name);
    assert name
    brief = extractBrief(blocks)
    print("brief = ", brief)
    assert brief

    assert valid(blocks)

    items = extractStructEle(blocks)
    print("struct items = ", items);
    writeStructToFile(brief, name, items, fout)

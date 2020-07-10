#!/usr/bin/python
# -*- coding: UTF-8 -*-

keyword=("\\brief", "\\param", "\\return")

#是否注释
def isComment(line):
    if line.strip().startswith("/") or line.strip().startswith("*"):
        return True
    return False 

def isHaskKey(line):
    if line.strip().startswith("#") :
        return True
    return False     

def extractBody(block) : 
    body = ""
    for line in block :
        if not isComment(line) and not isHaskKey(line) :
            body += line

    return body

def isContainKeyword(line) :
    for word in keyword:
        if word in line:
            return True
    
    return False

def extractBrief(block) : 
    
    word="\\brief "
    brief = ""
    start = -1
    num = len(block)
    for id in range(0, num):
        line = block[id].strip()
        if word in line :
            start = id + 1
            brief += line[line.find(word) + len(word):]
        elif id == start and  not isContainKeyword(block[id]) and line.startswith("//") :
            start +=1
            brief += line.strip('/')

    print("brief = " , brief)
    return brief

def extractCommentParams(block) : 

    word = "\\param "
    
    note = ""
    start = -1
    num = len(block)
    params=[]
    for id in range(0, num):
        line = block[id].strip()
        if word in line :

            if len(note.strip()) > 0:
                params.append(note.strip())
                note = ""
            start = id + 1

            note += line[line.find(word) + len(word):]
            

        elif id == start and  not isContainKeyword(block[id]) and line.startswith("//") :
            start +=1
            note += line.strip('/')
    
    if len(note.strip()) > 0:
        params.append(note.strip())

    kvs = []
    for param in params:
        tup = (param[: param.find('-')].strip(), param[param.find('-') + 1:].strip())
        kvs.append(tup)
                

    print("comment params = " , kvs)
    return kvs
        


def extractCommentRet(block) : 

    word = "\\return "
    
    retrval = ""
    start = -1
    num = len(block)
    rets=[]
    for id in range(0, num):
        line = block[id].strip()
        if word in line :

            if len(retrval.strip()) > 0:
                rets.append(retrval.strip())
                retrval = ""
            start = id + 1

            retrval += line[line.find(word) + len(word):]
            

        elif id == start and  not isContainKeyword(block[id]) and line.startswith("//") :
            start +=1
            retrval += retrval.strip('/')
    
    if len(retrval.strip()) > 0:
        rets.append(retrval.strip())
                

    print("return = " , rets)
    return rets
        



  
       

def parseBody(body) :

    params = body[body.rfind('(') : body.rfind(')') + 1];
    print(params)
    return params

def parseFuncName(body) :
    delParam = body[:body.rfind('(')]
    eles = delParam.split()
    name = eles[len(eles) - 1]
    return name

def parseParams(params) :
    params = params.strip("()")
    ps = params.split(',')

    print(ps)
    kv = []
    for param in ps:
        if len(param.strip()) > 0 and "[" not in param:
            tup = (param[:param.rfind(' ')].strip(), param[param.rfind(' '):].strip())
            kv.append(tup)
        elif len(param.strip()) > 0 and "["  in param:
            tup = (param[:param.rfind(' ')].strip() + "[]", param[param.rfind(' '): param.rfind('[')].strip())
            kv.append(tup)
    
    return kv
   

def mergeParams(commentParams, params):

    
    assert len(commentParams) == len(params) 
        
    

    resultVals=[]
    for commentVal,desc in commentParams:
        for typ, realVal in params:
            if realVal == commentVal:
                tvd=(typ, realVal, desc)
                resultVals.append(tvd)
                break

    print(resultVals)
    
    assert len(commentParams) == len(resultVals)
            
    
    return resultVals

    


def ansisFunctionBlock(block, fout):
   
    commentParams = extractCommentParams(block)
    rets = extractCommentRet(block)
    brief = extractBrief(block)

    body = extractBody(block)
    funcname = parseFuncName(body).strip("()*")
    print(funcname)
    params = parseParams(parseBody(body))

    print(params)
    resultParams = mergeParams(commentParams, params)

    fout.write('## ' + funcname + '\n\n')
    fout.write('*方法*\n```c++\n\n')
    fout.write(body)
    fout.write('\n```\n*功能描述*\n\n')
    fout.write(brief + "\n")

    if len(resultParams) > 0 :
        fout.write('\n\n*参数说明*\n\n')
        fout.write("| 参数      |    类型 | 描述  |\n| :-------- | --------:| :--: |\n")
   
   
    for p in resultParams:
        fout.write("|" + p[0] + "|" + p[1] + "|" + p[2] + "|\n")

    if len(rets) > 0 :
        fout.write('\n*返回值* ')
        fout.write("\n\n")

    for ret in rets :
        fout.write(ret +" ")

    fout.write('\n\n')
    print(body)

    
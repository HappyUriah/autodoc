#!/usr/bin/python
# -*- coding: UTF-8 -*-

keyword=("\\brief", "\\param", "\\return", "\\tparam")

cKeywork=("const", "explicit", "default", "static")

#是否是函数声明
def isFunction(strs):
    if "(" in strs and ")" in strs:
        return True
    else :
        return False

#是否注释
def isComment(line):
    if line.strip().startswith("/") or line.strip().startswith("*"):
        return True
    return False 


def isContainKeyword(line) :
    for word in keyword:
        if word in line:
            return True
    
    return False

# 解析描述语句
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

    #print("brief = " , brief)
    return brief

# 提取注释里面的参数信息
def extractCommentParams(block) : 

    word = "\\param "
    tword = "\\tparam "
    
    note = ""
    start = -1
    num = len(block)
    params=[]
    for id in range(0, num):
        line = block[id].strip()
        if word in line :
            #上一个提取完成
            if len(note.strip()) > 0:
                params.append(note.strip())
                note = ""
            start = id + 1

            note += line[line.find(word) + len(word):]
        elif tword in line:
            #上一个提取完成
            if len(note.strip()) > 0:
                params.append(note.strip())
                note = ""
            start = id + 1

            note += line[line.find(tword) + len(tword):]

            

        elif id == start and  not isContainKeyword(block[id]) and line.startswith("//") :
            start +=1
            note += line.strip('/')
    
    if len(note.strip()) > 0:
        params.append(note.strip())

    kvs = []
    for param in params:
        #print(param)
        assert param.find(' ') != -1
        tup = (param[: param.find(' ')].strip(), param[param.find(' ') + 1:].strip(' \n\t-'))
        kvs.append(tup)
                

    #print("comment params = " , kvs)
    return kvs
        


def extractCommentRet(block) : 

    word = " \\return "
    
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
            start = start + 1
            retrval += line.strip('/')
    
    if len(retrval.strip()) > 0:
        rets.append(retrval.strip())
                

    print("return = " , rets)
    return rets
        

#是否有返回值
def hasReturnValue(strs):

    delParam = strs[:strs.rfind('(')]
    eles = delParam.split()

    print("return num = ", len(eles))
    num = len(eles)
    retVal = "void"
    if num > 1 :
        retVal = eles[len(eles) - 2].strip()
    
    if retVal in cKeywork:
        retVal = "void"

    print("retVal = ", retVal)
    return retVal != "void"
  
def parseBody(strs):
    pos1 = strs.find(";")
    pos2 = strs.find("{")

    if pos2 != -1 :
        return strs[0:pos2]
    else :
        return strs[0:pos1]
       
# 解析实际参数
def parseRealParams(strs) :

    params = strs[strs.rfind('(') : strs.rfind(')') + 1];
    #print(params)
    return params

# 解析函数名称
def parseFuncName(strs) :
    delParam = strs[:strs.rfind('(')]
    eles = delParam.split()
    name = eles[len(eles) - 1].strip("()*")
    return name

# 解析参数项
def parseParamsItem(params) :
    params = params.strip("()")
    ps = params.split(',')

    #print(ps)
    kv = []
    for param in ps:
        param = param.strip()
        if len(param) > 0 and "[" not in param:
            assert param.find(' ') != -1
            tup = (param[:param.rfind(' ')].strip(), param[param.rfind(' '):].strip())
            kv.append(tup)
        elif len(param.strip()) > 0 and "["  in param:
            assert param.find(' ') != -1
            tup = (param[:param.rfind(' ')].strip() + "[]", param[param.rfind(' '): param.rfind('[')].strip())
            kv.append(tup)
    
    return kv
   

# 检查注释参数和实际参数是否匹配
def mergeParams(commentParams, params):

    
    assert len(commentParams) == len(params) 
        
    
    resultVals=[]
    for commentVal,desc in commentParams:
        for typ, realVal in params:
            if realVal == commentVal:
                tvd=(typ, realVal, desc)
                assert typ
                assert realVal
                assert desc
                resultVals.append(tvd)
                break

    print(resultVals)

    
    assert len(commentParams) == len(resultVals)
            
    return resultVals


def writeFunctionToFile(funcname, body, brief, mergeParamItems, commentRets, fout):
    fout.write('## ' + funcname + '\n\n')
    fout.write('*方法*\n```c++\n')
    fout.write(body)
    fout.write('\n```\n*功能描述*\n\n')
    fout.write(brief + "\n")

    if len(mergeParamItems) > 0 :
        fout.write('\n\n*参数说明*\n\n')
        fout.write("| 参数      |    类型 | 描述  |\n| :-------- | --------:| :--: |\n")
   
   
    for p in mergeParamItems:
        fout.write("|" + p[0] + "|" + p[1] + "|" + p[2] + "|\n")

    if commentRets and len(commentRets) > 0 :
        fout.write('\n*返回值* ')
        fout.write("\n\n")

        for ret in commentRets :
            fout.write(ret +" \n\n")

    fout.write('\n\n')



def ansisFunctionBlock(strs, blocks, fout, classname=None):

    strs = parseBody(strs).strip()

    # pos = strs.find('{')
    # if pos != -1:
    #     strs = strs[:pos]
    print("is function", strs)
   
    # commentParams = extractCommentParams(block)
    # rets = extractCommentRet(block)
    brief = extractBrief(blocks)
    assert brief
    print("brief = ", brief)

    realParams = parseRealParams(strs)
    print("realParams = ", realParams)

    paramItems = parseParamsItem(realParams)
    print("param items = ", paramItems)

    funcname = parseFuncName(strs)
    print("funcname = ", funcname)
    if classname :
        funcname = classname+"::"+funcname

    hasRetV = hasReturnValue(strs)


    commentParamItems = extractCommentParams(blocks)
    print("comment param items = ", commentParamItems)

    mergeParamItems = mergeParams(commentParamItems, paramItems)
    print(mergeParams)

    commentRets = extractCommentRet(blocks)

    if hasRetV :
        assert len(commentRets) > 0
        writeFunctionToFile(funcname, strs, brief, mergeParamItems, commentRets, fout)
    else :
        writeFunctionToFile(funcname, strs, brief, mergeParamItems, None, fout)
    




    
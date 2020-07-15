import funcParse as func

def isComment(line):
    return line.strip().startswith('//')

def isStatement(line) :
    return line.strip().endswith(';')

# def ansisBlock(strs, blocks):
    # if isEnum(strs):

    #     enum.ansisEnumBlock(strs, blocks)
    # elif isClass(strs):
    #     classParse.ansisClassBlock(strs, blocks)

def ansisClassBlock(strs, blocks):
    print("is class")
    num = len(blocks)

    start = 0
    for i in range(0, num):
        line = blocks[i].strip()
        if line and not isComment(line):
            start = i;
            break
    

    print("blocks[start] = ", blocks[start])

    assert blocks[start].find('{') != -1 and  blocks[start].find('}') == -1
    newblocks=[]
    newstrs=""
    for i in range(1 + start, num):
        line = blocks[i]
        if isComment(line):
            newblocks.append(line)
        elif isStatement(line):
            newblocks.append(line)
            newstrs = newstrs + line[:line.find('//')]
            if newstrs.count("{") == newstrs.count("}") :
                print(newstrs)
                print("###")
                print(newblocks)
                # ansisBlock(strs, blocks)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')
        else :
            newblocks.append(line)
            newstrs = newstrs + line[:line.find('//')]
            if newstrs.count("{") == newstrs.count("}") and newstrs.count('{') > 0 :
                print(newstrs)
                print("###")
                print(newblocks)
                # ansisBlock(strs, blocks)

                newstrs=""
                newblocks.clear()
                print('\n###################\n\n\n\n')


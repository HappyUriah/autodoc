import sys
import enumParse as enum
import structParse as struct
import funcParse as func
import classParse 
import otherParse as other


def isComment(line):
    return line.strip().startswith('//')


def isStatement(line) :

    if line.find('//') != -1 :
        return line[0:line.find('//')].strip().endswith(";")
    else :
        return line.strip().endswith(';')

def rmComment(line):
    if line.find("//") != -1 :
        return line[:line.find("//")]
    else :
        return line


def ansisBlock(strs, blocks, fout):
    if enum.isEnum(strs):
        enum.ansisEnumBlock(strs, blocks,fout)
    elif classParse.isClass(strs):
        classParse.ansisClassBlock(strs, blocks,fout)
    elif struct.isStruct(strs):
        
        struct.ansisStructBlock(strs,blocks, fout)
    
    elif func.isFunction(strs):
        func.ansisFunctionBlock(strs, blocks, fout)

    else :
        other.ansisOtherBlock(strs, blocks)

       
def rmMacroAndAnsis(input,output):


    f = open(sys.argv[1])               # 返回一个文件对象 
    line = f.readline()
    newlines = []

    while line:
        #print(line)
        if  line.strip().startswith('#') or line.strip().startswith('protected:')  or line.strip().startswith("public:") or line.strip().startswith('privated:') :
            pass
        elif line.strip().startswith("namespace "):
            pass
        else:
            newlines.append(line)
        line = f.readline()
    
    f.close()

    fout = open(output, "a+")
    

    blocks=[]
    strs=""


    for line in newlines:
        if isComment(line):
            blocks.append(line)
        elif isStatement(line):
            blocks.append(line)
            strs = strs + rmComment(line)
            if strs.count("{") == strs.count("}") :
                print(strs)
                print("###")
                print(blocks)
                ansisBlock(strs, blocks, fout)

                strs=""
                blocks.clear()
                print('\n###################\n\n\n\n')
        else :
            blocks.append(line)
            strs = strs + rmComment(line)
            if strs.count("{") == strs.count("}") and strs.count("{") > 0:
                print(strs)
                print("###")
                print(blocks)
                ansisBlock(strs, blocks, fout)

                strs=""
                blocks.clear()
                print('\n###################\n\n\n\n')
        

        if strs.count("{") < strs.count("}") :
            print(strs)
            strs=""
            blocks.clear()
            
            print('\n###################\n\n\n\n')





    fout.close()

    
    



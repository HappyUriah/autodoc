import sys
import enumParse as enum
import structParse as struct
import funcParse as func
import classParse 

def isComment(line):
    return line.strip().startswith('//')

def isStatement(line) :
    return line.strip().endswith(';')


    #return eles[0] == "enum" or (eles[0] == "typedef " and eles[1] == "enum")




def isClass(strs):

    if strs.strip().startswith("class ") and strs.count('{') > 0 :
        return True
    else :
        return False




def ansisBlock(strs, blocks):
    if enum.isEnum(strs):

        enum.ansisEnumBlock(strs, blocks)
    elif isClass(strs):
        pass
        #classParse.ansisClassBlock(strs, blocks)
    
    elif struct.isStruct(strs):
        
        struct.ansisStructBlock(strs,blocks)
    
    elif func.isFunction(strs):
        pass
        #func.ansisFunctionBlock(strs, blocks)

        #print("is enum")


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

blocks=[]
strs=""


for line in newlines:
    if isComment(line):
        blocks.append(line)
    elif isStatement(line):
        blocks.append(line)
        strs = strs + line[:line.find('//')]
        if strs.count("{") == strs.count("}") :
            print(strs)
            print("###")
            print(blocks)
            ansisBlock(strs, blocks)

            strs=""
            blocks.clear()
            print('\n###################\n\n\n\n')
    else :
        blocks.append(line)
        strs = strs + line[:line.find('//')]

    
    

    
   # print('#######')
    #print(line)




f.close()
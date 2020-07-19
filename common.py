#断言
def assertStr(ass, string):

    if not ass :
        print("\033[31m%s" % string)
        assert False 

#是不是注释行，
def isComment(line):
    return line.strip().startswith('//')

#是不是包含;
def isStatement(line) :

    if line.find('//') != -1 :
        return line[0:line.find('//')].strip().endswith(";")
    else :
        return line.strip().endswith(';')

#提取非注释语句
def rmComment(line):
    if line.find("//") != -1 :
        return line[:line.find("//")]
    else :
        return line
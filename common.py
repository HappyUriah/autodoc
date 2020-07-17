
def assertStr(ass, string):

    if not ass :
        print("\033[31m%s" % string)
        assert False 
    
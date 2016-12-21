import textwrap

def myWrap(inStr):
    ''' Wraps text
        inStr: input string that needs to be wrapped
        tmp: temporary string that has the output
    '''
    tmp = textwrap.wrap(inStr, 30)
    tmp = '\n'.join(tmp) 
    return tmp

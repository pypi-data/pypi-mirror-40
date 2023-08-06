import elist.elist as elel

LINE_SP = "\n"
NUL = "\x00"

def padding_line(line,width,null=NUL):
    return(line+null*(width-line.__len__()))

def padding_lines(lines,**kwargs):
    if('null' in kwargs):
        null = kwargs['null']
    else:
        null = NUL
    width = elel.max_length(lines)
    return(elel.mapv(lines,padding_line,[width,null]))

def oddize_line(line,**kwargs):
    if('null' in kwargs):
        null = kwargs['null']
    else:
        null = NUL
    cond = (line.__len__() % 2 == 0)
    if(cond):
        line = line[0:line.__len__() // 2] + null + line[line.__len__() // 2:]
    else:
        pass
    return(line)

def oddize_rows(lines,**kwargs):
    if('null' in kwargs):
        null = kwargs['null']
    else:
        null = NUL
    height = lines.__len__()
    lines = elel.mapv(lines,oddize_line,[null])
    cond = (height%2 == 0)
    if(cond):
        lines = lines[0:height//2] + [null * lines[0].__len__()]+ lines[height//2:]
    else:
        pass
    return(lines)

def no_oddize(lines,**kwargs):
    return(lines)




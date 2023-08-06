def get_wh(s,**kwargs):
    if('line_sp' in kwargs):
        line_sp = kwargs['line_sp']
    else:
        line_sp = "\n"
    lines = s.split("\n")
    height = lines.__len__()
    width = lines[0].__len__()
    return((height,width))



import elist.elist as elel
import estring.estring as eses
import cv2
import numpy as np
import pandas as pd
from sldghmmr4nut.lines import fmt

def img2df(img):
    height = img.shape[0]
    width = img.shape[1]
    channel = img.shape[2]
    pd_index = elel.init_range(0,height,1)
    pd_columns = elel.init_range(0,width,1)
    df = pd.DataFrame(img.tolist(),columns=pd_columns,index=pd_index)
    return(df)

def df2img(df):
    l = df.values.tolist()
    ndarr =  np.array(l)
    return(ndarr)


def ord2bgr(num):
    bgr = '{:0>6}'.format(hex(num)[2:])
    bgr = eses.divide(bgr,2)
    bgr = elel.mapv(bgr,int,[16])
    return(bgr)

def bgr2ord(bgr):
    def map_func(ele):
        ele = '{:0>2}'.format(hex(ele)[2:])
        return(ele)
    bgr = elel.mapv(bgr,map_func)
    num = elel.join(bgr,"")
    num = int(num,16)
    return(num)


def txt2bgrndarr(s,**kwargs):
    if('line_sp' in kwargs):
        line_sp = kwargs['line_sp']
    else:
        line_sp = fmt.LINE_SP
    if('null' in kwargs):
        null  = kwargs['line_sp']
    else:
        null = fmt.NUL
    if('oddize' in kwargs):
        oddize = kwargs['oddize']
    else:
        oddize = fmt.no_oddize
    lines = s.split(line_sp)
    lines = fmt.padding_lines(lines,null)
    lines = oddize(lines,null)
    char_lines = elel.mapv(lines,lambda line:list(line))
    mat= elel.mat_mapv(char_lines,ord)
    mat = elel.mat_mapv(mat,ord2bgr)
    ndarr = np.array(mat,dtype=np.uint8)
    return(ndarr)

def bgrndarr2txt(ndarr,**kwargs):
    if('line_sp' in kwargs):
        line_sp = kwargs['line_sp']
    else:
        line_sp = fmt.LINE_SP
    if('null' in kwargs):
        null  = kwargs['line_sp']
    else:
        null = fmt.NUL
    mat = ndarr.tolist()
    mat = elel.mat_mapv(mat,bgr2ord)
    lines = elel.mat_mapv(mat,chr)
    lines = elel.mapv(lines,lambda line:elel.join(line,""))
    s = elel.join(lines,line_sp)
    s = s.replace(null,"")
    return(s)

import elist.elist as elel
import estring.estring as eses
import numpy as np
import sldghmmr4nut.ndarr.do as ndo
import sldghmmr4nut.ndarr.convert as ndcvt
import os
import efdir.fs as fs

def wrap(s,fn,*args,**kwargs):
    ndarr = ndcvt.txt2ndarr(s,**kwargs)
    cond = (args[0] == [])
    if(cond):
        ndarr = fn(ndarr)
    else:
        ndarr = fn(ndarr,*args)
    s = ndcvt.ndarr2txt(ndarr)
    return(s)



def txtfilter(s,actions,**kwargs):
    actions = ndo.creat_action_list(actions,**kwargs)
    ndarr = ndcvt.txt2ndarr(s,**kwargs)
    ndarr = ndo.filter(ndarr,actions)
    s = ndcvt.ndarr2txt(ndarr)
    return(s)

def swap_dimension(s,**kwargs):
    s = wrap(s,ndo.swap_dimension,[],**kwargs)
    return(s)

def fliplr(s,**kwargs):
    s = wrap(s,np.fliplr,[],**kwargs)
    return(s)

def flipud(s,**kwargs):
    s = wrap(s,np.flipud,[],**kwargs)
    return(s)

def to_ancient_chinese(s,**kwargs):
    s = txtfilter(s,[ndo.swap_dimension,np.fliplr],**kwargs)
    return(s)

def from_ancient_chinese(s,**kwargs):
    s = txtfilter(s,[np.fliplr,ndo.swap_dimension],**kwargs)
    return(s)

def swap_row(s,rowseq1,rowseq2,**kwargs):
    s = wrap(s,ndo.swap_row,rowseq1,rowseq2,**kwargs)
    return(s)

def swap_rows(s,rowseqs1,rowseqs2,**kwargs):
    s = wrap(s,ndo.swap_rows,rowseqs1,rowseqs2,**kwargs)
    return(s)

def swap_col(s,colseq1,colseq2,**kwargs):
    s = wrap(s,ndo.swap_col,colseq1,colseq2,**kwargs)
    return(s)

def swap_cols(s,colseqs1,colseqs2,**kwargs):
    s = wrap(s,ndo.swap_cols,colseqs1,colseqs2,**kwargs)
    return(s)

def insert_row(s,rowseq,row,**kwargs):
    row = eses.str2chnums(row)
    s = wrap(s,ndo.insert_row,rowseq,row,**kwargs)
    return(s)

def insert_rows(s,rowseq,rows,**kwargs):
    rows = elel.mapv(rows,eses.str2chnums)
    s = wrap(s,ndo.insert_rows,rowseq,rows,**kwargs)
    return(s)

def insert_col(s,colseq,col,**kwargs):
    col = eses.str2chnums(col)
    s = wrap(s,ndo.insert_col,colseq,col,**kwargs)
    return(s)

def insert_cols(s,colseq,cols,**kwargs):
    cols = elel.mapv(cols,eses.str2chnums)
    s = wrap(s,ndo.insert_cols,colseq,cols,**kwargs)
    return(s)

def append_col(s,col,**kwargs):
    col = eses.str2chnums(col)
    s = wrap(s,ndo.append_col,col,**kwargs)
    return(s)

def append_cols(s,cols,**kwargs):
    cols = elel.mapv(cols,eses.str2chnums)
    s = wrap(s,ndo.append_cols,cols,**kwargs)
    return(s)

def append_row(s,row,**kwargs):
    row = eses.str2chnums(row)
    s = wrap(s,ndo.append_row,row,**kwargs)
    return(s)

def append_rows(s,rows,**kwargs):
    rows = elel.mapv(rows,eses.str2chnums)
    s = wrap(s,ndo.append_rows,rows,**kwargs)
    return(s)

def prepend_col(s,col,**kwargs):
    col = eses.str2chnums(col)
    s = wrap(s,ndo.prepend_col,col,**kwargs)
    return(s)

def prepend_cols(s,cols,**kwargs):
    cols = elel.mapv(cols,eses.str2chnums)
    s = wrap(s,ndo.prepend_cols,cols,**kwargs)
    return(s)

def prepend_row(s,row,**kwargs):
    row = eses.str2chnums(row)
    s = wrap(s,ndo.prepend_row,row,**kwargs)
    return(s)

def prepend_rows(s,rows,**kwargs):
    rows = elel.mapv(rows,eses.str2chnums)
    s = wrap(s,ndo.prepend_rows,rows,**kwargs)
    return(s)

def crop(s,top,left,bot,right,**kwargs):
    s = wrap(s,ndo.crop,top,left,bot,right,**kwargs)
    return(s)

def slct(s,rowseqs,colseqs,**kwargs):
    s = wrap(s,ndo.slct,rowseqs,colseqs,**kwargs)
    return(s)

def slct_col(s,colseq,**kwargs):
    s = wrap(s,ndo.slct_col,[colseq],**kwargs)
    return(s)

def slct_cols(s,colseqs,**kwargs):
    s = wrap(s,ndo.slct_cols,colseqs,**kwargs)
    return(s)

def slct_row(s,rowseq,**kwargs):
    s = wrap(s,ndo.slct_row,[rowseq],**kwargs)
    return(s)

def slct_rows(s,rowseqs,**kwargs):
    s = wrap(s,ndo.slct_rows,rowseqs,**kwargs)
    return(s)

def rows(s,**kwargs):
    s = wrap(s,ndo.rows,[],**kwargs)
    return(s)

def cols(s,**kwargs):
    s = wrap(s,ndo.cols,[],**kwargs)
    return(s)

def rplc_col(s,colseq,col,**kwargs):
    col = eses.str2chnums(col)
    s = wrap(s,ndo.rplc_col,colseq,col,**kwargs)
    return(s)

def rplc_cols(s,colseqs,cols,**kwargs):
    cols = elel.mapv(cols,eses.str2chnums)
    cols = np.array(cols)
    s = wrap(s,ndo.rplc_cols,colseqs,cols,**kwargs)
    return(s)

def rplc_row(s,rowseq,row,**kwargs):
    row = eses.str2chnums(row)
    s = wrap(s,ndo.rplc_row,rowseq,row,**kwargs)
    return(s)

def rplc_rows(s,rowseqs,rows,**kwargs):
    rows = elel.mapv(rows,eses.str2chnums)
    rows = np.array(rows)
    s = wrap(s,ndo.rplc_rows,rowseqs,rows,**kwargs)
    return(s)

def rplc_blk(s,top,left,bot,right,blk,**kwargs):
    blk = ndcvt.txt2ndarr(blk,**kwargs) 
    s = wrap(s,ndo.rplc_blk,top,left,bot,right,blk,**kwargs)
    return(s)

def rm_col(s,colseq,**kwargs):
    s = wrap(s,ndo.rm_col,[colseq],**kwargs)
    return(s)

def rm_cols(s,colseqs,**kwargs):
    s = wrap(s,ndo.rm_cols,[colseqs],**kwargs)
    return(s)

def rm_row(s,rowseq,**kwargs):
    s = wrap(s,ndo.rm_row,[rowseq],**kwargs)
    return(s)

def rm_rows(s,rowseqs,**kwargs):
    s = wrap(s,ndo.rm_rows,[rowseqs],**kwargs)
    return(s)

def ccwrot90(s,**kwargs):
    s = wrap(s,ndo.ccwrot90,[],**kwargs)
    return(s)

def ccwrot180(s,**kwargs):
    s = wrap(s,ndo.ccwrot180,[],**kwargs)
    return(s)

def ccwrot270(s,**kwargs):
    s = wrap(s,ndo.ccwrot270,[],**kwargs)
    return(s)

def cwrot90(s,**kwargs):
    s = wrap(s,ndo.cwrot90,[],**kwargs)
    return(s)

def cwrot180(s,**kwargs):
    s = wrap(s,ndo.cwrot180,[],**kwargs)
    return(s)

def cwrot270(s,**kwargs):
    s = wrap(s,ndo.cwrot270,[],**kwargs)
    return(s)

def rowtop_colleft(s,**kwargs):
    s = wrap(s,ndo.rowtop_colleft,[],**kwargs)
    return(s)

def rowtop_colright(s,**kwargs):
    s = wrap(s,ndo.rowtop_colright,[],**kwargs)
    return(s)

def rowbot_colright(s,**kwargs):
    s = wrap(s,ndo.rowbot_colright,[],**kwargs)
    return(s)

def rowbot_colleft(s,**kwargs):
    s = wrap(s,ndo.rowbot_colleft,[],**kwargs)
    return(s)

def rowleft_coltop(s,**kwargs):
    s = wrap(s,ndo.rowleft_coltop,[],**kwargs)
    return(s)

def rowright_coltop(s,**kwargs):
    s = wrap(s,ndo.rowright_coltop,[],**kwargs)
    return(s)

def rowright_colbot(s,**kwargs):
    s = wrap(s,ndo.rowright_colbot,[],**kwargs)
    return(s)

def rowleft_colbot(s,**kwargs):
    s = wrap(s,ndo.rowleft_colbot,[],**kwargs)
    return(s)

def quad_split(s,spt,**kwargs):
    ndarr = ndcvt.txt2ndarr(s,**kwargs)
    ndarrl = ndo.quad_split(ndarr,spt)
    stl,str,sbl,sbr = elel.mapv(ndarrl,ndcvt.ndarr2txt)
    return([stl,str,sbl,sbr])

####TEST4FUN####

def quad_smash(s,spt,**kwargs):
    if("char_width" in kwargs):
        char_width = kwargs["char_width"]
    else:
        if(ord(s[0])<=255):
            char_width = 1
        else:
            pass
    def display(blk_str):
        print(blk_str)
        print("-"* char_width* blk_str.split("\n")[0].__len__())
    arr = quad_split(s,spt,**kwargs)
    elel.mapv(arr,display)
    return(arr)


def quad_smash_txt(txt,spt,**kwargs):
    s = fs.rfile(txt)
    basename,suffix = os.path.splitext(os.path.basename(txt))
    tl,tr,bl,br = quad_smash(s,spt,**kwargs)
    fs.wfile(basename+".tl"+suffix,tl)
    fs.wfile(basename+".tr"+suffix,tr)
    fs.wfile(basename+".bl"+suffix,bl)
    fs.wfile(basename+".br"+suffix,br)
    return((s,tl,tr,bl,br))


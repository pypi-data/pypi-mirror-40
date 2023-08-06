import elist.elist as elel
import spaint.spaint as spaint

def names():
    lines = elel.init(11)
    lines[0] = " otl |               otop                     | otr "
    lines[1] = " ------------------------------------------------------------------------ "
    lines[2] = "              | etl | etop  | etr|               "
    lines[3] = "              ---------------------------------------------              "
    lines[4] = "              |               |           |               |               "
    lines[5] = "   ol   |   el   |   INNER   |   er  |   or  "
    lines[6] = "              |               |           |               |               "
    lines[7] = "              ---------------------------------------------               "
    lines[8] = "              | ebl | ebot  | ebr|               "
    lines[9] = " ------------------------------------------------------------------------ "
    lines[10] = " obl |               obot                     | obr "
    s = elel.join(lines,"\n")
    s = s.replace("otl",spaint.slpaint("out-top-left","blue",rtrn=True))
    s = s.replace("otr",spaint.slpaint("out-top-right","blue",rtrn=True))
    s = s.replace("obl",spaint.slpaint("out-bot-left","blue",rtrn=True))
    s = s.replace("obr",spaint.slpaint("out-bot-right","blue",rtrn=True))
    s = s.replace("otop",spaint.slpaint("out-top","green",rtrn=True))
    s = s.replace("ol",spaint.slpaint("out-left","green",rtrn=True))
    s = s.replace("obot",spaint.slpaint("out-bot","green",rtrn=True))
    s = s.replace("or",spaint.slpaint("out-right","green",rtrn=True))
    s = s.replace("etl",spaint.slpaint("edge-top-left","yellow",rtrn=True))
    s = s.replace("etr",spaint.slpaint("edge-top-right","yellow",rtrn=True))
    s = s.replace("ebl",spaint.slpaint("edge-bot-left","yellow",rtrn=True))
    s = s.replace("ebr",spaint.slpaint("edge-bot-right","yellow",rtrn=True))
    s = s.replace("etop",spaint.slpaint("edge-top","maroon",rtrn=True))
    s = s.replace("el",spaint.slpaint("edge-left","maroon",rtrn=True))
    s = s.replace("ebot",spaint.slpaint("edge-bot","maroon",rtrn=True))
    s = s.replace("er",spaint.slpaint("edge-right","maroon",rtrn=True))
    s = s.replace("INNER",spaint.slpaint("INNER","aqua",rtrn=True))
    print(s)

def ids():
    s = '''     0       |                   7                       |     6        
------------------------------------------------------------------------
             |     8         |   15      |     14        |              
             ---------------------------------------------              
             |               |           |               |              
     1       |     9         |   16      |      13       |      5       
             |               |           |               |              
             ---------------------------------------------              
             |     10        |    11     |    12         |              
------------------------------------------------------------------------
     2       |                     3                     |     4        '''
    print(s)

def abbrs():
    s = '''     zotl    |                   zotop                   |     zotr     
------------------------------------------------------------------------
             |     zetl      |   zetop   |     zetr      |              
             ---------------------------------------------              
             |               |           |               |              
     zol     |     zel       |   zinner  |     zer       |    zor       
             |               |           |               |              
             ---------------------------------------------              
             |     zebl      |   zebot   |    zebr       |              
------------------------------------------------------------------------
     zobl    |                 zobot                     |     zobr     '''
    print(s)

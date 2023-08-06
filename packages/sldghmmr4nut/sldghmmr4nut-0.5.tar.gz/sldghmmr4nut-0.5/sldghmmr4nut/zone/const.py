
ABBR_MD = {
    'zotl': 'zone-out-top-left',
    'zotr': 'zone-out-top-right',
    'zobl': 'zone-out-bottom-left',
    'zobr': 'zone-out-bottom-right',
    'zotop': 'zone-out-top',
    'zol': 'zone-out-left',
    'zor': 'zone-out-right',
    'zobot': 'zone-out-bottom',
    'zetl': 'zone-edge-top-left',
    'zetr': 'zone-edge-top-right',
    'zebl': 'zone-edge-bottom-left',
    'zebr': 'zone-edge-bottom-right',
    'zetop': 'zone-edge-top',
    'zel': 'zone-edge-left',
    'zer': 'zone-edge-right',
    'zebot': 'zone-edge-bottom',
    'zinner': 'zone-inner',
    'zone-out-top-left': 'zotl',
    'zone-out-top-right': 'zotr',
    'zone-out-bottom-left': 'zobl',
    'zone-out-bottom-right': 'zobr',
    'zone-out-top': 'zotop',
    'zone-out-left': 'zol',
    'zone-out-right': 'zor',
    'zone-out-bottom': 'zobot',
    'zone-edge-top-left': 'zetl',
    'zone-edge-top-right': 'zetr',
    'zone-edge-bottom-left': 'zebl',
    'zone-edge-bottom-right': 'zebr',
    'zone-edge-top': 'zetop',
    'zone-edge-left': 'zel',
    'zone-edge-right': 'zer',
    'zone-edge-bottom': 'zebot',
    'zone-inner': 'zinner'
}

ID_MD = {
    'zotl'  : 0,
    'zol'   : 1,
    'zobl'  : 2,
    'zobot' : 3,
    'zobr'  : 4,
    'zor'   : 5,
    'zotr'  : 6,
    'zotop' : 7,
    'zetl'  : 8,
    'zel'   : 9,
    'zebl'  : 10,
    'zebot' : 11,
    'zebr'  : 12,
    'zer'   : 13,
    'zetr'  : 14,
    'zetop' : 15,
    'zinner': 16,
    0: 'zotl',
    1: 'zol',
    2: 'zobl',
    3: 'zobot',
    4: 'zobr',
    5: 'zor',
    6: 'zotr',
    7: 'zotop',
    8: 'zetl',
    9: 'zel',
    10: 'zebl',
    11: 'zebot',
    12: 'zebr',
    13: 'zer',
    14: 'zetr',
    15: 'zetop',
    16: 'zinner'
}






def id2abbr(id):
    return(ID_MD[id])

def abbr2id(abbr):
    return(ID_MD[abbr])

def abbr2name(abbr):
    return(ABBR_MD[abbr])

def name2abbr(name):
    return(ABBR_MD[name])

def id2name(id):
    abbr = ID_MD[id]
    return(ABBR_MD[abbr])

def name2id(name):
    abbr = ABBR_MD[name]
    return(ID_MD[abbr])



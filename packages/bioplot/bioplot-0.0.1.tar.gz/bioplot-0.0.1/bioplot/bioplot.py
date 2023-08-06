import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib import cm

one_letter_to_three_letter = {
    'A' : 'ALA',
    'R' : 'ARG',
    'N' : 'ASN',
    'D' : 'ASP',
    'B' : 'ASX',
    'C' : 'CYS',
    'E' : 'GLU',
    'Q' : 'GLN',
    'Z' : 'GLX',
    'G' : 'GLY',
    'H' : 'HIS',
    'I' : 'ILE',
    'L' : 'LEU',
    'K' : 'LYS',
    'M' : 'MET',
    'F' : 'PHE',
    'P' : 'PRO',
    'S' : 'SER',
    'T' : 'THR',
    'W' : 'TRP',
    'Y' : 'TYR',
    'V' : 'VAL',}

# RasMol Color
'''
Amino Acid  Color      Triple        Amino Acid    Color  Triple
  ASP,GLU   bright red [230,10,10]     CYS,MET     yellow [230,230,0]
  LYS,ARG   blue       [20,90,255]     SER,THR     orange [250,150,0]
  PHE,TYR   mid blue   [50,50,170]     ASN,GLN     cyan   [0,220,220]
  GLY       light grey [235,235,235]   LEU,VAL,ILE green  [15,130,15]
  ALA       dark grey  [200,200,200]   TRP         pink   [180,90,180]
  HIS       pale blue  [130,130,210]   PRO         flesh  [220,150,130]
'''
one_letter_aa_to_index = {
    'A' : 0,
    'R' : 1,
    'N' : 2,
    'D' : 3,
    'B' : 4,
    'C' : 5,
    'E' : 6,
    'Q' : 7,
    'Z' : 8,
    'G' : 9,
    'H' : 10,
    'I' : 11,
    'L' : 12,
    'K' : 13,
    'M' : 14,
    'F' : 15,
    'P' : 16,
    'S' : 17,
    'T' : 18,
    'W' : 19,
    'Y' : 20,
    'V' : 12,}

index_to_color = np.array(
    [[200, 200, 200],
     [20, 90, 255],
     [0, 220, 220],
     [230, 10, 10],
     [230, 10, 10],
     [230, 230, 0],
     [230, 10, 10],
     [0, 220, 220],
     [0, 220, 220],
     [235, 235, 235],
     [130, 130, 210],
     [15, 130, 15],
     [15, 130, 15],
     [20, 90, 255],
     [230, 230, 0],
     [50, 50, 170],
     [220, 150, 130],
     [250, 150, 0],
     [250, 150, 0],
     [180, 90, 180],
     [50, 50, 170],
     [15, 130, 15]]) / 255

class Bioplot(object):
    def __init__(self, ax):
        self.ax = ax
        self.set_colorbar()

    def grid(self, *args, **kwargs):
        self.ax.grid(*args, **kwargs)
        
    def set_colorbar(self, cmap_name='bwr', vmin=None, vmax=None):
        self.cmap_name = cmap_name
        self.cmap = plt.get_cmap(cmap_name)
        self.norm = mpl.colors.Normalize(vmin=vmin, vmax=vmax)
        self.scalarMap = cm.ScalarMappable(norm=self.norm, cmap=self.cmap)

    def get_rgb(self, val):
        return self.scalarMap.to_rgba(val)
        
    def aaplot2d(self, seq: str, colors: list=None, autoscale: bool=True, max_width=50):
        aa_length = len(seq)
        height = aa_length // max_width + 1
        left = np.zeros(height)
        h_range = list(range(height))
        
        if isinstance(colors, list):
            colors = np.array(colors)

        for idx in range(max_width):
            column_indexes = np.array(np.arange(idx, aa_length, max_width))
            if colors is None:
                c = index_to_color[[one_letter_aa_to_index[seq[i]] for i in column_indexes]]
            else:
                c = self.get_rgb(colors[column_indexes])
                
            _y = np.zeros(height)
            for i in range(c.shape[0]):
                _y[i] = 1
            self.ax.barh(h_range, _y, 0.9, left=left, color=c, label="a")
            left += _y

        for h in h_range:
            for i in range(max_width):
                idx = h*max_width+i
                if aa_length <= idx:
                    break
                ax.text(i+0.5, h, seq[idx], family='monospace',
                        horizontalalignment='center', verticalalignment='center')

    def aaplot3d(self):
        raise NotImplementedError



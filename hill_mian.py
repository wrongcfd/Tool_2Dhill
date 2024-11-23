import numpy as np
import matplotlib.pyplot as plt
import math
import pandas as pd
import os
from hill_plotfuction import *

data_folder = 'Result'
dataset_files = [   
('FHill_X25_N20_H6_Z6_dt0.002_t_uv_lu10_Time_800000.txt'),
('FHill_X25_CAON40_H6_Z6_dt0.001_lu10_Time_400000.txt'),
] 
dataset_files = [os.path.join(data_folder, filename) for filename in dataset_files]
plt.rc('font', size=14)   
fig = plt.gcf()
fig.subplots_adjust(left=0.2, right=0.8, top=0.95, bottom=0.1)
colors = ['steelblue', 'pink', 'olive', 'black', 'red']
# colors = ['olive', 'black', 'violet', 'orange', 'black']
# colors = ['steelblue', 'violet', 'orange', 'violet', 'black']
line_styles = ['-', '--', '--', '--', '--']

plt.get_current_fig_manager().window.state('zoomed')

plt.subplot(2, 1, 1)
hillplot_Ux(dataset_files, line_styles, colors)
plt.ylim(0,6)
plt.xticks(np.arange(-1.25, 12.5, 1.25))

plt.subplot(2, 1, 2)
hillplot_Ruu(dataset_files, line_styles, colors)
plt.ylim(0,6)
plt.xticks(np.arange(-1.25, 12.5, 1.25))
    # plt.savefig('LBM_hill.png', bbox_inches='tight')
plt.show()
plt.close()
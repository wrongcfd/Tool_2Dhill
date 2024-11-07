# slicefunction.py
from slicefunction import HDF5ToTXTConverter
# 
#name = '_periodic0.00036_kp0.00001_setu0.88c_sponge_'
#folder = 'output202411'+'06222743'

name = '_periodic0.000566_kp0.00001_setu0.88c_sponge_'
folder = 'output202411071'+'40355'

converter = HDF5ToTXTConverter(folder, name)
converter.run()

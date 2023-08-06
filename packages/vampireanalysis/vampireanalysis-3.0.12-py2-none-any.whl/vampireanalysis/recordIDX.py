#!/usr/bin/env python

# built-in libraries
import os
from time import sleep
# external libraries
import pandas as pd
import numpy as np

def recordIDX(IDX,buildmodel,folder,cellornuc):
	print('## recordIDX.py')

	if buildmodel: 
		uiname = 'image sets to build model.csv'
	else: 
		uiname = 'image sets to apply model.csv'
	UI = pd.read_csv(os.path.join(folder,uiname))
	setpaths = UI['set location']

	# ledgername = cellornuc + '_object_ledger.csv'
	# picklename = cellornuc + '_boundary_coordinate_stack.pickle'

	if cellornuc == 'cells':
		ledgername = 'Cells_registry.csv'
		picklename = 'Cells_boundary_coordinate_stack.pickle'
	else: 
		ledgername = 'Nuclei_registry.csv'
		picklename = 'Nuclei_boundary_coordinate_stack.pickle'

	for setpath in setpaths:
		obj_ledger = pd.read_csv(os.path.join(setpath,ledgername))
		pkl = pd.read_pickle(os.path.join(setpath,picklename)).values
		pkl = pkl.flatten()
		setlength = len(pkl)
		obj_ledger['IDX']=pd.Series(IDX[0:setlength]) #write
		IDX = np.delete(IDX,range(setlength)) #remove
		obj_ledger.to_csv(os.path.join(setpath,ledgername))


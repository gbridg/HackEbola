#!/usr/bin/python
import sys
sys.path.append("../")

import pdb
import csv
import glob




def processDir(in_dir, out_dir):
    
    infilepath_list = glob.glob("%s*" % in_dir)
    
    for this_infilepath in infilepath_list:
        
        outfilepath = "%s.csv" % this_infilepath.replace('raw', 'csv')
        print this_infilepath, outfilepath
        
        csvReader = csv.reader(open(this_infilepath, 'rU'), delimiter = '\t', dialect=csv.excel_tab)
        csvWriter = csv.writer(open(outfilepath, 'wb'))        
        
        for row in csvReader:
            csvWriter.writerow(row)


in_dir  = 'data/raw/'
out_dir = 'data/csv/'
processDir(in_dir, out_dir)

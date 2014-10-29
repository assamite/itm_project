'''Compression and decompression with gzip.
'''
import os
import sys
import gzip

usage_text = 'Usage: python ' + __file__ + ' -[cd] data_folder out_folder'

if len(sys.argv) != 4:
    print usage_text
    sys.exit()
    
datafolder = sys.argv[2]
outfolder = sys.argv[3]

# Compression
if sys.argv[1] == '-c':
    for f in os.listdir(datafolder):
        fp = os.path.join(datafolder, f)
        if os.path.isfile(fp) and f[0] != ".":
            dp = os.path.join(outfolder, f + ".gz")
            print "Compressing {} to {}".format(fp, dp)
            fh = gzip.open(dp, 'w')
            fh.write(open(fp, 'r').read())
            fh.close()
    
# Decompression        
if sys.argv[1] == '-d':
    for f in os.listdir(datafolder):
        fp = os.path.join(datafolder, f)
        if os.path.isfile(fp) and f[0] != ".":
            dp = os.path.join(outfolder, f.rsplit(".", 1)[0])
            print "Decompressing {} to {}".format(fp, dp)
            fh = open(dp, 'w')
            fh.write(gzip.open(fp, 'r').read())
            fh.close()
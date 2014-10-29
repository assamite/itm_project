'''Compare file sizes in different folders.
'''
import os
import sys

usage_text = "Usage: python " + __name__ + " data_folder compress_folder1 compress_folder2 ..."

if len(sys.argv) < 3:
    print usage_text
    sys.exit()
    
folders = sys.argv[1:]
list_dirs = [os.listdir(fol) for fol in folders]
#file_lists = [[f if fol == folders[0] else f.rsplit(".", 1)[0] for f in os.listdir(fol) if os.path.isfile(os.path.join(fol, f)) and f[0] != '.'] for fol in folders]
# Files in all the folders, excluding files starting with dots. Not very readable..
# For compressed folders, the names are cut before last dot.
file_lists = [[f if ld == list_dirs[0] else f.rsplit(".", 1)[0] for f in ld] for ld in list_dirs]

# Get a set of common file names in all folders. 
common_files = set(file_lists[0])
for f in file_lists[1:]:
    common_files = common_files & set(f)
    
common_files = sorted(list(common_files))
# Some pretty print calculations
max_file_name = max([len(c) for c in common_files] + [len('Totals:')])
max_folder_name = max([len(f) for f in folders] + [20])
max_first = max([max_file_name, len("Original")])
mfn = str(max_folder_name)
output = ""
headline = ("{:<" + str(max_file_name) + "} ").format('File')
for f in folders:
    headline += ("{:<" + mfn + "} ").format(f)
    
output = headline + "\n"
    
sums = [0 for l in folders]
for c in common_files:
    original_file = os.path.join(folders[0], c)
    original_name = c
    original_size = os.stat(original_file).st_size
    sums[0] += original_size
    line = ("{:<" + str(max_file_name) + "} ").format(original_name)
    comp_part = "{} ({:.4f}%)".format(original_size, 100.0)
    comp_part = ("{:<" + mfn + "} ").format(comp_part)
    line += comp_part
    for i, folder in enumerate(folders[1:]):
        compressed_name = [f for f in list_dirs[i+1] if f.rsplit(".", 1)[0] == c][0]
        compressed_file = os.path.join(folder, compressed_name)
        compressed_size = os.stat(compressed_file).st_size
        compressed_percent = (float(compressed_size) / original_size) * 100 if original_size != 0 else 0.0
        sums[i+1] += compressed_size
        comp_part = "{} ({:.4f}%)".format(compressed_size, compressed_percent)
        comp_part = ("{:<" + mfn + "} ").format(comp_part)
        line += comp_part
    output += line + "\n"
 
procents = len(sums)
last_line = ("{:<" + str(max_file_name) + "} ").format("Totals:")
for s in sums:
    percent = (float(s) / sums[0]) * 100
    comp_part = "{} ({:.4f}%)".format(s, percent)
    comp_part = ("{:<" + mfn + "} ").format(comp_part)
    last_line += comp_part
        
output += last_line + "\n"
print output

        
        
    



    
    




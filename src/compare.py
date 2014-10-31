'''Compare file sizes in different folders.
'''
import os
import sys
import inspect

def compare(folders):
    """Compare file sizes in different folders. 
    
    Assumes that files in first folder represents original (non-compressed) data,
    and other folders contain compressed data files with names matching to 
    original data files appended by additional compression file suffix.
    
    That is, if original folder contains file name 'data.dat', other folders
    contain file names of the form  'data.dat.foo' but not 'data.dat.foo.bar'.
    Suffix can vary from folder to folder.
    
    May break if folders don't have any common files or there are files with
    zero length.
    """
    abspaths = [os.path.abspath(f) for f in folders]
    list_dirs = [os.listdir(fol) for fol in abspaths]
    # Files in all the folders, excluding files starting with dots.
    # For compressed folders, the names are cut before last dot.
    file_lists = [[f if ld == list_dirs[0] else f.rsplit(".", 1)[0] for f in ld if f[0] != '.'] for ld in list_dirs]
    
    # Get a set of common file names in all folders. 
    common_files = set(file_lists[0])
    map(lambda d: common_files.intersection(d), file_lists[:1])
  
    # Sort the names for pretty print
    common_files = sorted(list(common_files))
    # Some pretty print calculations
    max_file_name = max([len(c) for c in common_files] + [len('Totals:')])
    max_folder_name = max([len(f) for f in folders] + [20])
    mfn = str(max_folder_name)
    
    # Construct first line for output with folder names
    headline = ("{:<" + str(max_file_name) + "} ").format('File')
    for f in folders:
        headline += ("{:<" + mfn + "} ").format(f)
        
    output = headline + "\n"
        
    sums = [0 for i in xrange(len(folders))]
    # For every common file presented in the folders, get file size and size 
    # percentages of the original data for all folders.
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
     
    # Construct last line for output with file totals
    last_line = ("{:<" + str(max_file_name) + "} ").format("Totals:")
    for s in sums:
        percent = (float(s) / sums[0]) * 100
        comp_part = "{} ({:.4f}%)".format(s, percent)
        comp_part = ("{:<" + mfn + "} ").format(comp_part)
        last_line += comp_part
            
    output += last_line + "\n"
    return output, sums


if __name__ == "__main__":
    usage_text = "\n"
    usage_text += "Usage: python " + __file__ + " data_folder compress_folder1 compress_folder2 ..."
    usage_text += "\n\n"
    usage_text += compare.__doc__

    if len(sys.argv) < 3:
        print usage_text
        sys.exit()
    
    folders = sys.argv[1:]
    output, sums = compare(folders)
    print output
    
         
        
    



    
    




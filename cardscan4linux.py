#!/usr/bin/env python

# Modules
import re
import os
import sys
import argparse
import subprocess
from itertools import islice

# Input argument setup
p = argparse.ArgumentParser(description='Search Linux-based systems for Credit/Debiit Card numbers.')
p.add_argument('-o','--output',dest='output',help='Output data to a file instead of the Terminal.',action='store_true')
p.add_argument('-D','--max-depth',dest='depth',help='Enter the max depth that the scanner will search from the given directory (Default is 3).',type=int,default=3)
p.add_argument('-d','--min-depth',dest='mindepth',help='Enter the min depth that the scanner will search from the given directory (No Default).',type=int)
p.add_argument('-l','--lines',dest='lines',help='Enter the number of lines to cycle through (Default is 50)',type=int,default=50)
p.add_argument('-p','--path',help='Input the root-file path that you want to recursively search through, e.g. /var (Default is /)',default='/')
p.add_argument('-e','--extensions',dest='extensions',help='Input the file extensions that should be searched for.',required=True,nargs='+')
p.add_argument('-max','--max-size',help='Enter the maximum file-size to search for (Default 100 Kilobytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes',dest="maxsize",default="100k")
p.add_argument('-min','--min-size',help='Enter the minimum file-size to search for (Default 16 Bytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes',dest="minsize",default="16c")
p.add_argument('-mount','--scan-mount',dest='mounted',help='Enable to scan the mounted remote file systems (Default is off.)',required=False,action='store_true')
p.add_argument('-v','--verbose',dest='verbose',help='Display verbose messages (Warning: output can be huge).',required=False,action='store_true')
a = p.parse_args()

# String concatenation for file extension searching.
extCmd = ""
z = 0
for ext in a.extensions:
        if z == 0:
                extCmd = " -name '*.%s'" %(ext)
                z += 1
        else:
                extCmd = extCmd + (" -o -name '*.%s'" %(ext))
                z += 1

# Sizing
max = ("-size -" + a.maxsize) # Default 100 Kilobytes (100k)
min = ("-size +" + a.minsize) # Default 16 bytes (16 c)

# Exclude files (remote mounted files) that manage to sneak through the find -type f.
#y = 0
#exclCmd = ""
#exclList = ""
#os.system("df -h | grep : | cut -d '%' -f 2 | cut -d ' ' -f 2 > /tmp/cardscan4linux.exclude  2> /dev/null")
#exclude_lines = sum(1 for line in open('/tmp/cardscan4linux.exclude'))
#with open("/tmp/cardscan4linux.exclude","r") as exclude_file:
#        if exclude_lines > 1:
#                for exclude in exclude_file:
#                        if y == 0:
#                                exclCmd = ' \( ! -path "%s/*"' %(str(exclude.rstrip("\n")))
#                                exclList = (str(exclude.rstrip("\n")))
#                                y += 1
#                        else:
#                                exclCmd = (exclCmd + (' -o ! -path "%s/*"' %(str(exclude.rstrip("\n")))))
#                                exclList = exclList + " " + (str(exclude.rstrip("\n")))
#                exclCmd = (exclCmd + " \)")

# Output to stdout
print ("=========================================================")
print ("[ Root Path ] \t\t" + str(a.path))
print ("[ Max Size ] \t\t" + str(a.maxsize))
print ("[ Min Size ] \t\t" + str(a.minsize))
print ("[ Extensions ] \t\t" + str(a.extensions))
print ("[ Lines per file ] \t" + str(a.lines))
print ("[ Depth of search ] \t" + str(a.depth))
print ("[ Scan Mounted Dirs ] \t" + str(a.mounted))
print ("=========================================================")
print ("\n[*] Starting file-system scan. This may take a while...")

# Local or Remote Mounting
if a.mounted:
    remote_mount = ""
else:
    remote_mount = "-mount "

# Min depth
if a.mindepth is None:
    min_depth = ""
else:
    min_depth = "-mindepth %s " %(str(a.mindepth))

# Create a list of all files with the provided extensions
full_path_list = subprocess.check_output('find %s %s-maxdepth %s %s-type f \( %s \) %s %s ' %(a.path,remote_mount,a.depth,min_depth,extCmd,max,min), shell=True)
full_path_list = full_path_list.rstrip().split('\n')

# Count how many entries in the list file
# deprecated  file_lines = sum(1 for count_lines in open('/tmp/cardscan4linux.list'))
file_lines = len(full_path_list)

# Output to user
print ("[*] File-system search complete. " + str(file_lines) + " files to check for card-data.")

# Regex to filter card numbers
regexAmex = re.compile("([^0-9-]|^)(3(4[0-9]{2}|7[0-9]{2})( |-|)[0-9]{6}( |-|)[0-9]{5})([^0-9-]|$)") #16 Digit AMEX
regexVisa = re.compile("([^0-9-]|^)(4[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")
regexMaster = re.compile("([^0-9-]|^)(5[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")

# Log file - counting
total_count = 0

# Search through files in the list
try:
        for filepath in full_path_list:
                filepath = filepath.rstrip('\n')
                try:
                        with open(filepath) as file:
                                if a.verbose:
                                        print filepath
                                total_count += 1
                                with open('/tmp/cardscan4linux.log', 'w') as log_file:
                                        log_file.write(str(file_lines) + "/" + str(total_count) + "\n")
                
                                i = 0
                                results = []
                                head = list(islice(file, a.lines)) # Opens 50 lines by default
                
                                # Loops through each item in list
                                for item in head:
                                        # Prints if matches AMEX
                                        if re.match(regexAmex, item.rstrip('\n')):
                                                i += 1
                                                results.append("\tAMEX:\t\t " + item.rstrip('\n'))
        
        
                                        # Prints if matches VISA
                                        elif re.match(regexVisa, item.rstrip('\n')):
                                                i += 1
                                                results.append("\tVISA:\t\t " + item.rstrip('\n'))
                
                                        # Prints if matches Mastercard
                                        elif re.match(regexMaster, item.rstrip('\n')):
                                                i += 1
                                                results.append("\tMASTERCARD:\t " + item.rstrip('\n'))
                
                                if i > 0:
					if a.output:
						with open('cardscan.output', "a") as outfile:
							outfile.write("File: " + filepath + "\n")
							for result in results:
								outfile.write(result + "\n")
					else:
                                        	print ("File: " + filepath)
                                        	for result in results:
                                        	        print result
						
                except KeyboardInterrupt:
                        break
except:
        sys.exit("\r[*] There are no files that match the search.")
        
# Removes the temp file
try:
        os.remove("/tmp/cardscan4linux.log")
except OSError:
        pass


# End of file
print ("[*] Card scanning complete. " + str(file_lines) + " total files were scanned.")
if a.output:
	print ("[*] Output saved to " + (os.path.dirname(os.path.realpath(__file__))) + "/cardscan.output.")

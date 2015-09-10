#!/usr/bin/env python

# Modules
import re
import os
import sys
import argparse
from itertools import islice

# Input argument setup
p = argparse.ArgumentParser(description='Search Linux-based systems for Credit/Debiit Card numbers.')
# Will be added soon #p.add_argument('-f','--file',dest='filepath',help='Enter the file-path to search through.')
# Will be added soon #p.add_argument('-o','--output',dest='output',help='Path to output data instead of stdout.')
p.add_argument('-d','--depth',dest='depth',help='Enter the max depth that the scanner will go to from the root "/" directory (Default is 3).',type=int,default=3)
p.add_argument('-l','--lines',dest='lines',help='Enter the number of lines to cycle through (Default is 50)',type=int,default=50)
p.add_argument('-p','--path',help='Input the root-file path that you want to recursively search through, e.g. /var (Default is /)',default='/')
p.add_argument('-e','--extensions',dest='extensions',help='Input the file extensions that should be searched for.',required=True,nargs='+')
p.add_argument('-max','--max-size',help='Enter the maximum file-size to search for (Default 100 Kilobytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes',dest="maxsize",default="100k")
p.add_argument('-min','--min-size',help='Enter the minimum file-size to search for (Default 100 Bytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes',dest="minsize",default="100c")
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
max = ("-size -" + a.maxsize) # Default 100k
min = ("-size +" + a.minsize) # Default 1k

# Output to stdout
print ("Starting file-system scan. This may take a while...")

# Create a list of all files with the provided extensions
os.system('find %s -maxdepth %s -type f \( -name "*.txt"%s \) %s %s > /tmp/cardscan4linux.list' %(a.path,a.depth,extCmd,max,min))

# Count how many entries in the list file
file_lines = sum(1 for count_lines in open('/tmp/cardscan4linux.list'))

# Output to user
print ("File-system search complete. " + str(file_lines) + " files to check for card-data.")

# Regex to filter card numbers
regexAmex = re.compile("([^0-9-]|^)(3(4[0-9]{2}|7[0-9]{2})( |-|)[0-9]{6}( |-|)[0-9]{5})([^0-9-]|$)") #16 Digit AMEX
regexVisa = re.compile("([^0-9-]|^)(4[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")
regexMaster = re.compile("([^0-9-]|^)(5[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")

# Log file - counting
total_count = 0

# Search through files in the list
with open("/tmp/cardscan4linux.list", "r") as filelist:
    for filepath in filelist:
        filepath = filepath.rstrip('\n')

	with open(filepath) as file:
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
				results.append("\tAMEX: " + item.rstrip('\n'))


  		        # Prints if matches VISA
			elif re.match(regexVisa, item.rstrip('\n')):
				i += 1
				results.append("\tVISA: " + item.rstrip('\n'))

		        # Prints if matches Mastercard
			elif re.match(regexMaster, item.rstrip('\n')):
				i += 1
				results.append("\tMASTERCARD: " + item.rstrip('\n'))

		if i > 0:
			print ("File: " + filepath)
			for result in results:
				print result

# Removes the temp file
os.remove("/tmp/cardscan4linux.list")
os.remove("/tmp/cardscan4linux.log")

# End of file
print ("\nCard scanning complete. " + str(file_lines) + " total files were scanned.")

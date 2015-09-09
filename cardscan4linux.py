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
a = p.parse_args()

# Create a list of all files with the provided extensions
os.system('find / -maxdepth %s -type f \( -name "*.doc" -o -name "*.txt" -o -name "*.csv" \) > /tmp/file.list' %(a.depth))

# Regex to filter card numbers
regexAmex = re.compile("([^0-9-]|^)(3(4[0-9]{2}|7[0-9]{2})( |-|)[0-9]{6}( |-|)[0-9]{5})([^0-9-]|$)") #16 Digit AMEX
regexVisa = re.compile("([^0-9-]|^)(4[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")
regexMaster = re.compile("([^0-9-]|^)(5[0-9]{3}( |-|)([0-9]{4})( |-|)([0-9]{4})( |-|)([0-9]{4}))([^0-9-]|$)")

# Search through files in the list
with open("/tmp/file.list", "r") as filelist:
    for filepath in filelist:
        filepath = filepath.rstrip('\n')

	with open(filepath) as file:
		i = 0
		results = []
		head = list(islice(file, a.lines)) # Opens 50 lines

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
os.remove("/tmp/file.list")

# CardScan4Linux
Use this script to search through locally stored files for any Credit/Debit card details.

# Help
## Usage 
`cardscan4linux.py [-h] [-d DEPTH] [-l LINES] [-p PATH] -e EXTENSIONS [EXTENSIONS ...] [-max MAXSIZE] [-min MINSIZE]`

##optional arguments:
* `-h, --help` Show this help message and exit
* `-o, --output` Output data to a file instead of the Terminal.
* `-d DEPTH, --max-depth DEPTH` Enter the max depth that the scanner will go to from the root "/" directory (Default is 3).
* `  -d MINDEPTH, --min-depth MINDEPTH` Enter the min depth that the scanner will search from the given directory (No Default).
* `-l LINES, --lines LINES` Enter the number of lines to cycle through (Default is 50)
* `-p PATH, --path PATH`  Input the root-file path that you want to recursively search through, e.g. /var (Default is /)
* `-e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]` Input the file extensions that should be searched for.
* `-max MAXSIZE, --max-size MAXSIZE` Enter the maximum file-size to search for (Default 100 Kilobytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes
* `-min MINSIZE, --min-size MINSIZE` Enter the minimum file-size to search for (Default 16 Bytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes
* `-mount, --scan-mount` Enable to scan the mounted remote file systems (Default is off).
* `-v, --verbose` Display verbose messages (Warning: output can be huge).


# Example Output
`[root@sc ~]# ./cardscan4linux.py -e txt -d 8`
<br>`===================================`
<br>`[ Root Path ] 		/`
<br>`[ Max Size ] 100k`
<br>`[ Min Size ] 16c`
<br>`[ Extensions ] ['txt']`
<br>`[ Lines per file ] 50`
<br>`[ Depth of search ] 8`
<br>`===================================`

<br>`[*] Starting file-system scan. This may take a while...`
<br>`[*] File-system search complete. 24855 files to check for card-data.`
<br>`File: /home/carddetails.txt`
<br>`	AMEX:		 371449635398431`
<br>`	AMEX:		 371427352388125`
<br>`File: /root/test.txt`
<br>`	AMEX:		 378282246310005`
<br>`	AMEX:		 371449635398431`
<br>`	AMEX:		 378734493671000`
<br>`	MASTERCARD:	 5105105105105100`
<br>`	VISA:		 4111111111111111`
<br>`	VISA:		 4012888888881881`
<br>`	MASTERCARD:	 5522131028402823`

`[*] Card scanning complete. 24855 total files were scanned in 8 seconds.`


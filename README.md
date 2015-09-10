# CardScan4Linux
Use this script to search through locally stored files for any Credit/Debit card details.

# Help
## Usage 
`cardscan4linux.py [-h] [-d DEPTH] [-l LINES] [-p PATH] -e EXTENSIONS [EXTENSIONS ...] [-max MAXSIZE] [-min MINSIZE]`

##optional arguments:
* `-h, --help`            show this help message and exit
* `-d DEPTH, --depth DEPTH` Enter the max depth that the scanner will go to from the root "/" directory (Default is 3).
* `-l LINES, --lines LINES` Enter the number of lines to cycle through (Default is 50)
* `-p PATH, --path PATH`  Input the root-file path that you want to recursively search through, e.g. /var (Default is /)
* `-e EXTENSIONS [EXTENSIONS ...], --extensions EXTENSIONS [EXTENSIONS ...]` Input the file extensions that should be searched for.
* `-max MAXSIZE, --max-size MAXSIZE` Enter the maximum file-size to search for (Default 100 Kilobytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes
* `-min MINSIZE, --min-size MINSIZE` Enter the minimum file-size to search for (Default 16 Bytes). Units: "c" for bytes, "k" for Kilobytes, "M" for Megabytes


# Example Output
`sh-3.2# ./cardscan4linux.py -e txt csv`
<br>`File: /totesnotcardstuff.csv`
<br>`	MASTERCARD: 5531574632215548`
<br>`	MASTERCARD: 5302389081962467`
<br>`	MASTERCARD: 5284063636623906`
<br>`	MASTERCARD: 5497784457046850`
<br>`	MASTERCARD: 5409506380613721`
<br>`File: /Users/adam/card.txt`
<br>`	VISA: 4716976190795672`
<br>`	VISA: 4539212215411631`
<br>`	VISA: 4024007103533591`
<br>`	VISA: 4813399462194858`
<br>`	VISA: 4024007146779565`

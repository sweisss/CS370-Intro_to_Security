# Setup Info
To create [venv](https://docs.python.org/3/library/venv.html):
```
python -m venv /path/to/new/virtual/environment
```

To activate venv:

```
source venv/Scripts/activate
```

To activate WSLvenv:

```
source WSLvenv/bin/activate
```

To activate venv on Mac or flip:
```
source venv/bin/activate
```

To deactivate venv:

```
deactivate
```
#### Python version
WSL: 3.8.10

Mac: 3.10.10

## Organize the directory
Ensure that the project directory contains the follwing files
- *bloomFilter.py*
- *rockyou.ISO-8859-1.txt*
- *dictionary.txt*
- *requirements.txt*

> __NOTE:__ The text file names are currently hard coded in *bloomFilter.py* and thus
> need to be in the same directory and use the same names as stated here for
> the program to run properly. 

## Set up the environment
Set up your venv using your preferred methods. Suggestions can be found at the top of 
this page. 

Once the venv is activated, install the necessary dependencies by running the following
command:
```
pip install -r requirements.txt
```

# Run the program
From the project directory enter the following command:
```
python bloomFilter.py
```
Information will be printed to the console. Expect the entire program to take
about 3-5 minutes to run. 

## Modify the program
To change the preferences such as the target false positive probability,
to change the hash method used, or to activate debugging mode,
open *bloomFilter.py* in a text editor and change the values of the constants
at the top of the file. 

`DEBUG` mode will limit the size of `rockyou` and `dictionary` to 10000 words
(or whatever limit you decide to change it to), as well as print out additional
statements to the console. 

## What this program does
This program builds a Bloom Filter based on input parameters (hard coded),
then loads the filter with the over 14 million words from *rockyou.ISO-8859-1.txt*.
After loading the Bloom Filter, the program then uses the words in *dictionary.txt*
to check the accuracy of the Bloom Filter. The class `StatisticsTracker` keeps track
of the counts of True Positives, True Negatives, False Positives, and False Negatives
and prints out the results. 

More information can be found in the associated .pdf report. 

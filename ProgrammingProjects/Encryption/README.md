To activate venv:

```
source WSLvenv/bin/activate
```

To deactivate venv:

```
deactivate
```

OpenSSL version 1.1.1f  31 Mar 2020

Python version 3.8.10

## Section 3.4 Instructions
- Ensure that the file *progProj1_3.4.py* is in the same directory as *words.txt*.
- Activate your venv
- If [`Crypto.Cipher`](https://pycryptodome.readthedocs.io/en/latest/src/cipher/classic.html#cbc-mode) is not installed, follow the [installation instuctions](https://pycryptodome.readthedocs.io/en/latest/src/installation.html).
- The known plaintext and ciphertext are hard-coded in the program for this assignment:
    ```
    PLAINTEXT = "This is a top secret."
    CIPHER_STR = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"
    ```
- To run the program, simply navigate your shell (venv) to the directory containing it and enter:
    ```
    python progProj1_3.4.py
    ```
### Expected Results
The output should look like the following:
```
Found a match
Known Ciphertext: 8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9
Calculated Ciphertext: 8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9
Known plaintext: This is a top secret.
Calculated plaintext: This is a top secret.
Keyword: median
```

## Section 3.8 Instructions
- Ensure that he file *progProj1_3.8.py* is in the current directory of your command line shell. 
- Activate your venv
- If [`Crypto.Hash`](https://pycryptodome.readthedocs.io/en/latest/src/hash/hash.html) is not installed,
follow the [installation instuctions](https://pycryptodome.readthedocs.io/en/latest/src/installation.html).
- To run the program, simply navigate your shell (venv) to the directory containing it and enter:
    ```
    python progProj1_3.8.py
    ```
- There are two levels of debug print statements that can be controlled with the constants `DEBUG` and `DEBUG_2`
at the top of the script. These will include printouts of the messages and hashes as well as notifications of collisions. 
- The [MD5](https://pycryptodome.readthedocs.io/en/latest/src/hash/md5.html) hash method is used.
This can be replaced with another hash hash method if desired in the `main()` function.
### Expected Results
The output should look like the following:
```
Testing MD5 weak collision resistance.
---------------------------------------
MD5 weak collision resistance test results:
Total rounds: 100
Trials per round: 1000
Average number of trials needed for collision: 429.1154

Testing MD5 strong collision resistance.
---------------------------------------
MD5 strong collision resistance test results:
Total rounds: 100
Trials per round: 1000
Average number of trials needed for collision: 40.4400

Overall results
---------------------------------------
Average number of trials needed to break weak collision resistance: 429.1154
Average number of trials needed to break strong collision resistance: 40.4400
Strong collision property is easier to break using the brute force method.
```
Contrary to what one might assume, the strong collision resistance property, aslo known as the collision-free property,
is easier to break than the weak collision resistance property (also known as the one-way property).
To understand this, it's better to think of the properties as "one-way" and "collision-free" rather than "weak" or "strong".
It is harder for a hash algorithm to provide a "collision-free" hash since there is an infinite number of potential inputs
which result in a finite number of outputs.
Therefore, a *stronger* hash algorithm will take *more* trials to break the "strong" collision property than a weaker
hash algorithm (not to be confused with the weak collision resistance propterty). 

Another way to think about this is to use the [Birthday Problem](https://en.wikipedia.org/wiki/Birthday_problem). 
It is much harder to find a person with the same birthday as you (one-way aka weak collision resistance)
than it is to find two random people that have the same birthday (collision-free aka strong collision resistance).

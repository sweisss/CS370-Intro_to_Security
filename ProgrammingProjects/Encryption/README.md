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
- The known cyphertext and plaintext are hard-coded in the program for this assignment:
    ```
    CIPHER_STR = "8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9"
    PLAINTEXT = "This is a top secret."
    ```
- To run the program, simply navigate your shell (venv) to the directory containing it and enter:
    ```
    python progProj1_3.4.py
    ```

- The output should look like the following:
    ```
    Found a match
    Known Ciphertext: 8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9
    Calculated Ciphertext: 8d20e5056a8d24d0462ce74e4904c1b513e10d1df4a2ef2ad4540fae1ca0aaf9
    Known plaintext: This is a top secret.
    Calculated plaintext: This is a top secret.
    Keyword: median
    ```

## Section 3.8 Instructions

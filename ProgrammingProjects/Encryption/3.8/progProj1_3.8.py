"""
Seth Weiss
weissse@oregonstate.edu
CS 370 - Intro to Security
Fall 2023

Description:
In this task, we will investigate the difference between a hash function's two properties: weak 
collision resistance property versus strong collision-resistance property. You will use the brute-
force method to see how long it takes to break each of these properties. Instead of using 
OpenSSL's command-line tools, you are required to write your own programs to invoke the message 
digest functions in OpenSSL's crypto library.

To make the task feasible, we reduce the length of the hash value to 24 bits. We can use any one-way hash 
function, but we only use the first 24 bits of the hash value in this task. Namely, we are using a 
modified one-way hash function.

- How many trials will it take to break the weak collision resistance property using 
the brute-force method? You should repeat your experiment for multiple times (100 or more 
depending on how long each trial takes), and report your average number of trials.  

- How many trials will it take you to break the collision-free property using the brute-
force method? Similarly, you should report the average.  

- Based on your observation, which property is easier to break using the brute-force 
method?  

- Can you explain the difference in your observations?

Resources:
https://pycryptodome.readthedocs.io/en/latest/src/hash/hash.html
https://pycryptodome.readthedocs.io/en/latest/src/hash/hash.html#extensible-output-functions-xof
https://pycryptodome.readthedocs.io/en/latest/src/hash/md5.html
https://www.baeldung.com/cs/hash-collision-weak-vs-strong-resistance#:~:text=Weak%20Collision%20Resistance,is%20not%20a%20trivial%20task.
"""
from Crypto.Hash import SHA256, MD5, SHA512, SHA3_512

N_BITS = 24
N_BYTES = N_BITS // 8
TRIALS = 1000
DEBUG = False


debug_print = lambda input: print(input) if DEBUG else 0


def create_short_hash(data, hash_method):
    hasher = hash_method.new(data=str(data).encode())
    hash_hex = hasher.hexdigest()
    short_hash_hex = hash_hex[0:N_BYTES]
    return short_hash_hex


def test_hash_collisions(n:int, hash_method:object) -> int:
    hashlist = []
    collision_count = 0
    for i in range(n):
        hash_hex = create_short_hash(i, hash_method)
        if hash_hex in hashlist:
            debug_print(f"Collision detected on hash: {hash_hex}")
            collision_count += 1

        hashlist.append(hash_hex)

    return collision_count


def main():
    md5_collisions = test_hash_collisions(TRIALS, MD5)
    print(f'Total MD5 collisions after {TRIALS} trials: {md5_collisions}')

    sha256_collisions = test_hash_collisions(TRIALS, SHA256)
    print(f'Total SHA256 collisions after {TRIALS} trials: {sha256_collisions}')

    sha512_collisions = test_hash_collisions(TRIALS, SHA512)
    print(f'Total SHA512 collisions after {TRIALS} trials: {sha512_collisions}')

    sha3_512_collisions = test_hash_collisions(TRIALS, SHA3_512)
    print(f'Total SHA3_512 collisions after {TRIALS} trials: {sha3_512_collisions}')

if __name__ == "__main__":
    main()

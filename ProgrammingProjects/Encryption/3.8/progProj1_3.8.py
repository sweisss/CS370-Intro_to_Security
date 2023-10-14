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
from Crypto.Hash import SHA256, SHAKE128, MD5
import random

N_BITS = 24
N_BYTES = N_BITS // 8
TRIALS = 500
DEBUG = False


debug_print = lambda input: print(input) if DEBUG else 0


# sha = SHA256.new(data=b'First')
# print(type(sha))
# print(sha.hexdigest())

# shake = SHAKE128.new(data=b'First')
# print(type(shake))
# print(shake.read(N_BYTES).hex())

# md5 = MD5.new()
# md5.update(b'Hello')
# print(md5.hexdigest())


plaintext = random.randint(0, 100)
plaintext_b = str(plaintext).encode()

# debug_print(f'plaintext: {plaintext}')
# debug_print(f'plaintext_b: {plaintext_b}')

hashlist = []

def create_md5_hash(data):
    # data = str(data).encode()
    md5 = MD5.new(data=str(data).encode())
    hash_hex = md5.hexdigest()
    short_hash_hex = hash_hex[0:N_BYTES]
    return short_hash_hex


def test_md5_collisions(n:int):
    collision_count = 0
    for i in range(n):
        hash_hex = create_md5_hash(i)
        if hash_hex in hashlist:
            debug_print(f"Collision detected on hash: {hash_hex}")
            collision_count += 1

        hashlist.append(hash_hex)

    return collision_count


def main():
    md5_collisions = test_md5_collisions(TRIALS)
    print(f'Total MD5 collisions after {TRIALS} trials: {md5_collisions}')


if __name__ == "__main__":
    main()


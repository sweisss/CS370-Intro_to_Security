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
https://www.geeksforgeeks.org/python-os-urandom-method/
"""
from Crypto.Hash import SHA256, MD5, SHA512, SHA3_512
import os


N_BITS = 24
N_BYTES = N_BITS // 8
TRIALS = 1000
EXPERIMENTS = 100
DEBUG = True


debug_print = lambda input: print(input) if DEBUG else 0


def create_short_hash(data, hash_method):
    hasher = hash_method.new(data=data)
    hash_hex = hasher.hexdigest()
    short_hash_hex = hash_hex[0:N_BYTES]
    return short_hash_hex


def test_weak_collision_resistance(message, n_trials:int, hash_method:object) -> int:
    """
    The definition of weak collision resistance is: 
        given an input X and a hashing function H(), it is very difficult to find
        another input X` on which H(X) = H(X`).

        In other words, with an input X as the parameter, replicating the hash H(X)
        with another input X` is not a trivial task.

    Definition from baeldung.com link above.
    """
    collision_count = 0

    control_hash = create_short_hash(message, hash_method)
    debug_print(f'control_hash: {control_hash}')

    for i in range(n_trials):
        # Generate a random message to compare with the control message
        rand_msg = os.urandom(N_BITS)
        hash_hex = create_short_hash(rand_msg, hash_method)

        if control_hash == hash_hex:
            debug_print(f"Collision detected on trial {i} with hash: {control_hash} == {hash_hex}")
            collision_count += 1
        
    return collision_count


def test_strong_collision_resistance(n_trials:int, hash_method:object) -> int:
    """
    The main idea behind strong collision resistance is: 
        given a hashing function H() and two arbitrary inputs X and Y, there exists
        an absolute minimum chance of H(X) being equal to H(Y).

    In the case of strong collision resistance, we do not have a parameter to
    search for a collision as in the weak collision resistance.

    Definition from baeldung.com link above.
    """
    collision_count = 0

    for i in range(n_trials):
        # Generate two random messages for each trial
        msg_1 = os.urandom(N_BITS)
        msg_2 = os.urandom(N_BITS)

        # Ensure the messages are distinct
        while msg_1 == msg_2:
            msg_2 = os.urandom(N_BITS)
        
        hash_1 = create_short_hash(msg_1, hash_method)
        hash_2 = create_short_hash(msg_2, hash_method)

        if hash_1 == hash_2:
            debug_print(f"Collision detected on trial {i} with hash: {hash_1} == {hash_2}")
            collision_count += 1

    return collision_count


def main():
    print()
    print("Testing MD5 weak collision resistance.")
    print("---------------------------------------")
    weak_collisions = {}
    for i in range(EXPERIMENTS):
        weak_message = b'Testing weak collision resistance.'
        md5_collisions_1 = test_weak_collision_resistance(weak_message, TRIALS, MD5)
        if md5_collisions_1 > 0:
            weak_collisions[i] = md5_collisions_1
            debug_print(f'Total weak MD5 collisions after {i} rounds: {md5_collisions_1}')
            
    total_weak_collisions = sum(weak_collisions.values())
    avg_weak_collisions = total_weak_collisions / len(weak_collisions.values())

    print('MD5 weak collision cesistance Test results:')
    print(f'Total rounds: {EXPERIMENTS}')
    print(f'Trials per round: {TRIALS}')
    print(f"Total collisions: {total_weak_collisions}")
    print(f"Averge collisions per round: {avg_weak_collisions}")

    # print(f"MD5 Weak Collision Resistance Test resulted in {total_weak_collisions} "
    #       f"total collisions after 100 rounds of {TRIALS} trials each.")

    print()
    print("Testing MD5 strong collision resistance.")
    print("----------------------------------------")
    md5_collisions_2 = test_strong_collision_resistance(TRIALS, MD5)
    print(f'Total strong MD5 collisions after {TRIALS} trials: {md5_collisions_2}')


if __name__ == "__main__":
    main()

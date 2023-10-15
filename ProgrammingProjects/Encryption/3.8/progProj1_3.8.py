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
DEBUG_2 = False


debug_print = lambda input: print(input) if DEBUG else 0
debug_print_2 = lambda input: print(input) if DEBUG_2 else 0


def get_module_name(module):
    name = module.__name__.split(".")[2]
    return name


def create_short_hash(data, hash_method):
    hasher = hash_method.new(data=data)
    hash_hex = hasher.hexdigest()
    short_hash_hex = hash_hex[0:N_BYTES]
    return short_hash_hex


def test_weak_collision_resistance(n_trials:int, hash_method:object, **kwargs) -> int:
    """
    The definition of weak collision resistance is: 
        given an input X and a hashing function H(), it is very difficult to find
        another input X` on which H(X) = H(X`).

        In other words, with an input X as the parameter, replicating the hash H(X)
        with another input X` is not a trivial task.

    Definition from baeldung.com link above.

    Return: number of trials it takes to find a collision
    """
    message = kwargs['message']
    control_hash = create_short_hash(message, hash_method)
    debug_print_2(f'control_hash: {control_hash}')

    for i in range(1, n_trials + 1):
        # Generate a random message to compare with the control message
        rand_msg = os.urandom(N_BITS)
        hash_hex = create_short_hash(rand_msg, hash_method)

        if control_hash == hash_hex:
            debug_print(f'Collision detected on trial {i} with hash: {control_hash} == {hash_hex}')
            debug_print_2(f'Controll message: {message.hex()}; Compare message: {rand_msg.hex()}')
            return i
        
    return 0


def hashlist_contains_hash(hashlist, hash_1, hash_2):
    if hash_1 in hashlist:
        debug_print(f'hash_1 is already in hashlist: {hash_1}')
        debug_print_2(f'hashlist: {hashlist}')
        return True
    
    if hash_2 in hashlist:
        debug_print(f'hash_2 is already in hashlist: {hash_2}')
        debug_print_2(f'hashlist: {hashlist}')
        return True
    
    return False


def test_strong_collision_resistance(n_trials:int, hash_method:object, **kwargs) -> int:
    """
    The main idea behind strong collision resistance is: 
        given a hashing function H() and two arbitrary inputs X and Y, there exists
        an absolute minimum chance of H(X) being equal to H(Y).

    In the case of strong collision resistance, we do not have a parameter to
    search for a collision as in the weak collision resistance.

    Definition from baeldung.com link above.

    Return: number of trials it takes to find a collision
    """
    hashlist =[]
    for i in range(1, n_trials + 1):
        # Generate two random messages for each trial
        msg_1 = os.urandom(N_BITS)
        msg_2 = os.urandom(N_BITS)

        # Ensure the messages are distinct
        while msg_1 == msg_2:
            msg_2 = os.urandom(N_BITS)
        
        hash_1 = create_short_hash(msg_1, hash_method)
        hash_2 = create_short_hash(msg_2, hash_method)

        if hashlist_contains_hash(hashlist, hash_1, hash_2):
            return i

        if hash_1 == hash_2:
            debug_print(f'Collision detected on trial {i} with hash: {hash_1} == {hash_2}')
            debug_print_2(f'msg_1: {msg_1.hex()}, msg_2: {msg_2.hex()}')
            return i
        
        hashlist.extend([hash_1, hash_2])

    return 0


test_options = {'weak': test_weak_collision_resistance, 'strong': test_strong_collision_resistance}


def run_experiment(collision_property:str, hash_method, control_msg=''):
    """
    Runs an experiment N times for M trials and prints the results.

    param collision_property: 'weak' or 'strong'. Used to termine which test to run.
    param hash_method: python package such as MD5 or SHA256
    param control_msg: optional control message to be hashed in the weak collision test.

    return: average number of trials needed to find a collision throughout the experiment.
    """
    mod_name = get_module_name(hash_method)
    print()
    print(f'Testing {mod_name} {collision_property} collision resistance.')
    print('---------------------------------------')

    trials_counts = {}
    for i in range(EXPERIMENTS):
        trials_needed = test_options[collision_property](TRIALS, hash_method, message=control_msg)
        if trials_needed > 0:
            trials_counts[f'Round {i}'] = trials_needed
            debug_print(f'Collision found in round {i} after {trials_needed} trials.')
            
    avg_trials_needed = sum(trials_counts.values()) / len(trials_counts.values())

    print('---------------------------------------')
    print(f'{mod_name} {collision_property} collision resistance test results:')
    print(f'Total rounds: {EXPERIMENTS}')
    print(f'Trials per round: {TRIALS}')
    print(f'Average number of trials needed for collision: {avg_trials_needed:.4f}')

    return avg_trials_needed


def main():
    weak_message = b'Testing weak collision resistance.'
    weak_trials = run_experiment('weak', MD5, control_msg=weak_message)
    strong_trials = run_experiment('strong', MD5)

    print()
    if weak_trials < strong_trials:
        print('Weak collision property is easier to break using the brute force method.')
    elif strong_trials < weak_trials:
        print('Strong collision propety is easier to break using the brute force method.')
    else:
        print('Weak and strong collisoin properties are equally easy to break using brute force method.')

    weak_trials = run_experiment('weak', SHA256, control_msg=weak_message)
    strong_trials = run_experiment('strong', SHA256)

    print()
    if weak_trials < strong_trials:
        print('Weak collision property is easier to break using the brute force method.')
    elif strong_trials < weak_trials:
        print('Strong collision propety is easier to break using the brute force method.')
    else:
        print('Weak and strong collisoin properties are equally easy to break using brute force method.')

if __name__ == "__main__":
    main()

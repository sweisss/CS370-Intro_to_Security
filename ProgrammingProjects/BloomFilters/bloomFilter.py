"""
Seth Weiss
weissse@oregonstate.edu
CS 370 - Intro to Security
Fall 2023
Programming Project 2  - Bloom Filters

Project Requirements:
- The software will implement a Bloom filter.
- Bloom filter will be loaded with values from rockyou.txt.
- The software will automate the testing of values in dictionary.txt.
- The software will calculate and display statistics on true positive, 
    true negative, false positive, and false negative for the dictionary.txt 
    based on the rockyou.txt.

Design Considerations:
- Decide how big of a bit array you will use and understand the impact
    of such a decision.
- Decide how many hashing algorithms you will use and understand the impact
    of such a decision.
- Understand the difference between true positive, true negative, false positive,
    and false negative in relation to the results of a Bloom Filter.
- Check out the runtime difference between using a List and a SortedSet when you are
    comparing which values in dictionary.txt are in rockyou.txt (re: reference statistics).
    
Sources:
https://hur.st/bloomfilter/
https://hur.st/bloomfilter/?n=14344391&p=0.1&m=&k=
https://hur.st/bloomfilter/?n=14344391&p=0.075&m=&k=
https://www.youtube.com/watch?v=gBygn3cVP80
https://www.interviewcake.com/concept/java/bloom-filter
https://pycryptodome.readthedocs.io/en/latest/src/hash/sha256.html
"""
import math
from Crypto.Hash import SHA256, MD5, SHA512, SHA3_512
import timeit


########################################################
# Constants can be modified to affect the performance. #
########################################################
P = 0.01
HASH_METHOD = MD5

DEBUG = False
DEBUG_LIST_LEN = 10000
########################################################

def debug_print(input):
    if DEBUG:
        print(input)


class BloomFilter:
    """
    BloomFilter class manages and maintains a Bloom Filter.
    
    Parameters:        
        n : int
            Number of different elements (inputs) in the Bloom Filter.
        
        p : float
            Probability of false positives, fraction between 0 and 1 indicating 1-in-p.

        m : int
            Determines the size of the Bloom Filter's bitmap.

        k : int
            Number of hash functions to use.
            
        hash_method : module
            Takes a hashing module such as SHA256, SHA512, MD5, etc.
    """
    def __init__(self, n=None, p=0.1, m=None, k=None, hash_method=None) -> None:
        self.num_elements = n
        self.bitmap_size = self.set_optimal_size(n, p) if m is None else m
        self.prob_false_pos = p
        self.bitmap = self._build_base(self.bitmap_size)        
        self.num_hash_funcs = self.set_optimal_k(self.bitmap_size, self.num_elements) if k is None else k
        self.hash_method = hash_method
        self.hash_name = self.get_hash_name(hash_method)
        
    def get_hash_name(self, hash_method):
        if not hash_method:
            raise Exception('please specify a hash method')
        return hash_method.__name__.split(".")[2]
        
    def _build_base(self, bitmap_size):
        return [0] * bitmap_size

    def set_optimal_size(self, n, p) -> None:
        """
        n : Number of different elements (inputs) in the Bloom Filter
        p : Probability of false positives
        """
        return math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))

    def set_optimal_k(self, m, n):
        """
        m : Size of the Bloom Filter's bitmap
        n : Number of different elements (inputs) in the Bloom Filter
        """
        return round((m / n) * math.log(2))
        
    def _convert_string_to_hashed_int(self, element:str):
        element = str(element)
        return int(self.hash_method.new(element.encode('utf-8')).hexdigest(), 16)
        
    def determine_addrs(self, element) -> list:
        """
        Creates a list of bitmap addresses based on the bitmap size and
        the pre-determined number of hash functions k (self.num_hash_funcs)
        """
        int_val = self._convert_string_to_hashed_int(element)
        func = lambda k : (k * int_val + k) % self.bitmap_size
        
        return [func(k) for k in range(1, self.num_hash_funcs + 1)]
        
    def insert(self, element) -> None:
        """
        Inserts an element into the Bloom Filter.
        
        Hashes the elemen value and flips the corresponding bits.
        """
        addrs = self.determine_addrs(element)
        for addr in addrs:
            self.bitmap[addr] = 1
            
    def is_in_filter(self, element) -> bool:
        """
        Takes an element and checkes the filter for the associated bits. 
        
        If one of the bits is 0, the element has not been yet been added.
        If all of the bits are 1, the element might have been added, or it
        might be a false positive.
        """
        addrs = self.determine_addrs(element)
        for addr in addrs:
            if self.bitmap[addr] != 1:
                return False
        
        return True


class StatisticsTracker:
    """
    Keeps track of the counts and statistics of a Bloom Filter
    """
    def __init__(self) -> None:
        self.counts = {'True Positives': [],
                        'True Negatives': [],
                        'False Positives': [],
                        'False Negatives': []}
                    
    def reset_statistics(self):
        for k in self.counts.keys():
            self.counts[k].clear()

    def print_statistics(self):        
        total_words = sum([len(v) for v in self.counts.values()])

        for k, v in self.counts.items():
            print(f'{k}: {len(v)} words; {(len(v) / total_words * 100):.2f}%')

        tp_fp_ratio = len(self.counts["True Positives"]) / len(self.counts["False Positives"])
        print(f'Ratio of True to False Positives: {tp_fp_ratio:.2f}')

    def check_validity(self, input_set, checklist, bf:BloomFilter):
        """
        Checks the bitmap of a Bloom Filter against a set of inputs and a list of words to check.

        imput_set: A set of known inputs to the Bloom Filter
        
        checklist: A list of words to check against the Bloom Filter's bitmap
        """
        self.reset_statistics()
        
        # Ensure that the input_set is actually a set and not a list
        input_set = set(input_set)
                
        for word in checklist:
            # Check if the word is in the Bloom Filter
            is_in_bf = bf.is_in_filter(word)
            is_in_rockyou = word in input_set
            # If the word is not in the Bloom Filter
            if not is_in_bf:
                # If the word is not in the Bloom Filter nor in rockyou
                if not is_in_rockyou:
                    self.counts['True Negatives'].append(word)
                # A Bloom Filter should never return a false negative
                elif is_in_rockyou:
                    self.counts['False Negatives'].append(word)
            # If the word is in the Bloom Filter
            elif is_in_bf:
                # If the word is in the Bloom Filter but not in rockyou
                if not is_in_rockyou:
                    self.counts['False Positives'].append(word)
                else:
                    self.counts['True Positives'].append(word)
                    # Remove the word from the input_set to make the next lookup slightly faster
                    input_set.remove(word)
                    debug_print(f'removed word {word}')
                    debug_print(f'input_set len: {len(input_set)}')
                    
        assert sum([len(v) for v in self.counts.values()]) == len(checklist)


def load_words(file: str) -> list:
    """
    Loads words from a text file.
    Removes the newline character but retains any leading or trailing whitespace.
    """
    with open(file, 'r', encoding='latin-1') as f:
        words = [word.replace('\n', '') for word in f.readlines()]

    return words


def main():
    start_load_words_time = timeit.default_timer()

    print('Loading words from text files. This may take a minute...')

    rockyou = load_words('./rockyou.ISO-8859-1.txt')
    dictionary = load_words('./dictionary.txt')

    rockyou = rockyou[0:DEBUG_LIST_LEN] if DEBUG else rockyou
    dictionary = dictionary[0:DEBUG_LIST_LEN] if DEBUG else dictionary
    
    rockyou_set = set(rockyou)
    
    debug_print(rockyou[0:10])
    print(f'Words in rockyou: {len(rockyou_set)}')

    finish_load_words_time = timeit.default_timer()
    print(f'Total time to load files: {(finish_load_words_time - start_load_words_time):.4f} seconds')
    
    bf = BloomFilter(n=len(rockyou), p=P, hash_method=HASH_METHOD)
    debug_print(f'bitmap_size: {bf.bitmap_size}')
        
    debug_print('--------')
    print(f'Loading rockyou into Bloom Filter using {bf.num_hash_funcs} variations of hash method {bf.hash_name} '\
          f'with target collision probability p = {P} (1 in {int(1 / P)})...')
    debug_print('--------')

    start_bf_insert = timeit.default_timer()
    
    for word in rockyou:
        bf.insert(word)
    
    finish_bf_insert = timeit.default_timer()    
    
    print('All words in rockyou loaded to Bloom Filter')
    print(f'{sum(bf.bitmap)} of {(len(bf.bitmap))} bits are used. ({(sum(bf.bitmap)/len(bf.bitmap)):.2f}%)')
    print(f'Total time to fill Bloom Filter: {(finish_bf_insert - start_bf_insert):.4f} seconds')

    debug_print('--------')
    print('Checking dictionary words in Bloom Filter...')
    debug_print('--------')

    start_checking_dictionary = timeit.default_timer()
    
    stat_tracker = StatisticsTracker()
    stat_tracker.check_validity(rockyou_set, dictionary, bf)

    finish_checking_dictionary = timeit.default_timer()

    debug_print('--------')
    print('Finished checking dictionary words in Bloom Filter')
    print('Results')
    print('--------')
    stat_tracker.print_statistics()
    print(f'Total words in dictionary.txt: {len(dictionary)}')

    print(f'Total time checking dictionary: {(finish_checking_dictionary - start_checking_dictionary):.4f} seconds')
    print(f'Total time running program: {(finish_checking_dictionary - start_load_words_time):.4f} seconds')


if __name__ == "__main__":
    main()

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


DEBUG = False
DEBUG_LIST_LEN = 10000


def debug_print(input):
    if DEBUG:
        print(input)


class BloomFilter:
    """
    BloomFilter class manages and maintains a Bloom Filter.
    
    Parameters:
        m : int
            Determines the size of the Bloom Filter's bitmap.
        
        n : int
            Number of different elements (inputs) in the Bloom Filter.
            
        p : float
            Probability of false positives.
            
        k : int
            Number of hash functions to use.
            
        hash_method : module
            Takes a hashing module such as SHA256, SHA512, MD5, etc.
    """
    def __init__(self, m=64, n=None, p=0.1, k=3, hash_method=None) -> None:
        self.bitmap_size = int(m)
        self.num_elements = self.set_optimal_size(m, p) if n is None else n
        self.prob_false_pos = p
        self.num_hash_funcs = k
        self.bitmap = self._build_base()
        self.hash_method = hash_method
        self.hash_name = self.get_hash_name(hash_method)
        self.counts = {'True Positives': [],
                       'True Negatives': [],
                       'False Postives': [],
                       'False Negatives': []}
        
    def get_hash_name(self, hash_method):
        if not hash_method:
            raise Exception('please specify a hash method')
        return hash_method.__name__.split(".")[2]
        
    def _build_base(self):
        return [0] * self.bitmap_size

    def set_optimal_size(self, n, p) -> None:
        """
        n : Number of different elements (inputs) in the Bloom Filter
        p : Probability of false positives
        """
        self.bitmap_size = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))
        
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
    
    def reset_statistics(self):
        for k, _ in self.counts.items():
            self.counts[k].clear()

    def print_statistics(self):        
        total_words = sum([len(v) for v in self.counts.values()])

        for k, v in self.counts.items():
            print(f'{k}: {len(v)} words; {(len(v) / total_words * 100):.2f}%')

    def check_validity(self, input_set, checklist):
        """
        Checks the bitmap against a set of inputs and a list of words to check.
        """
        self.reset_statistics()
        
        # Ensure that the input_set is actually a set and not a list
        input_set = set(input_set)
                
        for word in checklist:
            # Check if the word is in the Bloom Filter
            is_in_bf = self.is_in_filter(word)
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
                    self.counts['False Postives'].append(word)
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
    
    bf = BloomFilter(m=len(rockyou), p=0.1, hash_method=MD5)
    debug_print(f'bitmap_size: {bf.bitmap_size}')
        
    debug_print('--------')
    print(f'Loading rockyou into Bloom Filter using hash method {bf.hash_name}...')
    debug_print('--------')

    start_bf_insert = timeit.default_timer()
    
    for word in rockyou:
        bf.insert(word)
    
    finish_bf_insert = timeit.default_timer()    
    
    print('All words in rockyou loaded to Bloom Filter')
    print(f'{sum(bf.bitmap)} of {(len(bf.bitmap))} bits are used.')
    print(f'Total time to fill Bloom Filter: {(finish_bf_insert - start_bf_insert):.4f} seconds')

    debug_print('--------')
    print('Checking dictionary words in Bloom Filter...')
    debug_print('--------')

    start_checking_dictionary = timeit.default_timer()
    
    bf.check_validity(rockyou_set, dictionary)

    finish_checking_dictionary = timeit.default_timer()

    debug_print('--------')
    print('Finished checking dictionary words in Bloom Filter')
    bf.print_statistics()
    print(f'Total words in dictionary.txt: {len(dictionary)}')

    print(f'Total time checking dictionary: {(finish_checking_dictionary - start_checking_dictionary):.4f} seconds')
    print(f'Total time running program: {(finish_checking_dictionary - start_load_words_time):.4f} seconds')


if __name__ == "__main__":
    main()

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
            
        structure : string
            Determines the underlying data structure of the Bloom Filter.
            Options are 'list' for a list-based Bloom Filter or 
            'set' for a sorted set. 
            TODO: decide if using sorted(set) is appropriate
                or if using the the SortedSet class is better
                https://grantjenks.com/docs/sortedcontainers/sortedset.html

    TODO: Be more descriptive.
    """
    def __init__(self, m=64, n=None, p=0.1, k=3, structure='list') -> None:
        self.bitmap_size = int(m)
        self.num_elements = self.set_optimal_size(m, p) if n is None else n
        self.prob_false_pos = p
        self.num_hash_funcs = k
        self.structure = structure
        self.bitmap = self._build_base()
        
    def _build_base(self):
        if self.structure == 'list':
            return [0] * self.bitmap_size
        elif self.structure == 'set':
            return {}
        else:
            raise Exception(f"unrecognized structure option: '{self.structure}'")
        
    def set_optimal_size(self, n, p) -> None:
        """
        n : Number of different elements (inputs) in the Bloom Filter
        p : Probability of false positives
        m : Number of bits in Bloom Filter        
        """
        self.bitmap_size = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))
        
    def _convert_string_to_SHA256_int(self, element:str):
        return int(SHA256.new(element.encode('utf-8')).hexdigest(), 16)
        
    def determine_addrs(self, element) -> list:       
        int_val = self._convert_string_to_SHA256_int(element)
        func = lambda k : (k * int_val) % self.bitmap_size
        
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
    
    def check_validity(self, input_set, checklist):
        """
        Checks the bitmap against a set of inputs and a list of words to check.
        """
        true_pos = []
        true_neg = []
        false_pos = []
        false_neg = []
        
        # Ensure that the input_set is actually a set and not a list
        input_set = set(input_set)
                
        for word in checklist:
            # Check if the word is in the Bloom Filter
            is_in_bf = self.is_in_filter(word)
            # If the word is not in the Bloom Filter
            if not is_in_bf:
                is_in_rockyou = word in input_set
                # If the word is not in the Bloom Filter nor in rockyou
                if not is_in_rockyou:
                    true_neg.append(word)
                # A Bloom Filter should never return a false negative
                elif is_in_bf:
                    false_neg.append(word)
            # If the word is in the Bloom Filter
            elif is_in_bf:
                is_in_rockyou = word in input_set
                # If the word is in the Bloom Filter but not in rockyou
                if is_in_rockyou is False:
                    false_pos.append(word)
                else:
                    true_pos.append(word)
                    # Remove the word from the input_set to make the next lookup slightly faster
                    input_set.remove(word)
                    debug_print(f'removed word {word}')
                    debug_print(f'input_set len: {len(input_set)}')
                    
        assert len(true_pos) + len(true_neg) + len(false_pos) + len(false_neg) == len(checklist)
                    
        return true_pos, true_neg, false_pos, false_neg


def load_words(file: str) -> list:
    """
    Loads words from a text file.
    Removes the newline character but retains any leading or trailing whitespace.
    """
    with open(file, 'r', encoding='latin-1') as f:
        words = [word.replace('\n', '') for word in f.readlines()]

    return words



def main():
    rockyou = load_words('./rockyou.ISO-8859-1.txt')
    dictionary = load_words('./dictionary.txt')

    rockyou = rockyou[0:DEBUG_LIST_LEN] if DEBUG else rockyou
    dictionary = dictionary[0:DEBUG_LIST_LEN] if DEBUG else dictionary
    
    rockyou_set = set(rockyou)
    
    debug_print(rockyou[0:10])
    print(f'len(rockyou): {len(rockyou)}')
    
    bf = BloomFilter(m=len(rockyou), p=0.1, structure='list')
    debug_print(f'bitmap_size: {bf.bitmap_size}')
        
    debug_print('--------')
    print('Loading rockyou into Bloom Filter')
    debug_print('--------')
    for word in rockyou:
        bf.insert(word)
        
    print('All words in rockyou loaded to Bloom Filter')
    print(f'{sum(bf.bitmap)} of {(len(bf.bitmap))} bits are used.')
    
    debug_print('--------')
    print('Checking dictionary words in Bloom Filter')
    debug_print('--------')
    
    true_pos, true_neg, false_pos, false_neg = bf.check_validity(rockyou_set, dictionary)

    debug_print('--------')
    print('Finished checking dictionary words in Bloom Filter')
    print(f'True Negatives: {len(true_neg)}')
    print(f'False Negatives: {len(false_neg)}')
    print(f'True Positives: {len(true_pos)}')
    print(f'False Postives: {len(false_pos)}')
    print(f'Total words in dictionary.txt: {len(dictionary)}')
    assert len(dictionary) == len(true_neg) + len(false_neg) + len(true_pos) + len(false_pos)
    

if __name__ == "__main__":
    main()

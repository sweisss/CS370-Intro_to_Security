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
https://hur.st/bloomfilter/?n=14344391&p=0.01&m=&k=3
https://www.youtube.com/watch?v=gBygn3cVP80
https://www.interviewcake.com/concept/java/bloom-filter
"""
import math

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
    def __init__(self, m=64, n=666, p=0.01, k=3, structure='list'):
        self.bitmap_size = int(m)
        self.num_elements = n
        self.prob_false_pos = p
        self.num_hash_funcs = k
        self.structure = structure
        self.filter = self._build_base()
        
    def _build_base(self):
        if self.structure == 'list':
            return []
        elif self.structure == 'set':
            return {}
        else:
            raise Exception(f"unrecognized structure option: '{self.structure}'")
        
    def set_optimal_size(self, n, p):
        """
        n : Number of different elements (inputs) in the Bloom Filter
        p : Probability of false positives
        m : Number of bits in Bloom Filter        
        """
        self.bitmap_size = math.ceil((n * math.log(p)) / math.log(1 / math.pow(2, math.log(2))))

        

def load_words(file: str) -> list:
    with open(file, 'r', encoding='latin-1') as f:
        words = [word.strip() for word in f.readlines()]

    return words


def main():
    rockyou = load_words('./rockyou.ISO-8859-1.txt')
    # print(rockyou[0:10])
    print(len(rockyou))
    
    bf = BloomFilter(structure='list')
    bf.set_optimal_size()
    

if __name__ == "__main__":
    main()

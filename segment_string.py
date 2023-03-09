import csv
from typing import List, Tuple
from math import log


# create word to cost dictionary based on word frequencies
cost_dict = {}
with open('./word_freq.csv') as freq_file:
    reader = csv.DictReader(freq_file)
    full_count = 0
    for row in reader:
        full_count += int(row['count'])
        cost_dict[row['word']] = int(row['count'])

# calculate cost as the -log(probability of word) based on the supplied word frequency file
for word in cost_dict:
    cost_dict[word] = -log(cost_dict[word]/full_count)

def segment(s: str) -> List[str]:
    "segment string using dynamic programming to keep track of the best word match at each string index"

    def get_word_cost(word: str) -> Tuple[str, int]:
        "return word cost based on preconfigured dictionary"
        return cost_dict.get(word, 9e99)

    def lowest_cost(i: int) -> Tuple[int, int]:
        "return lowest cost word based on string index"
        possible_words = enumerate(reversed(costs_by_idx))
        matches = []
        for idx, cost_by_idx in possible_words:
            matches.append((cost_by_idx[0] + get_word_cost(s[i - idx - 1:i]), idx + 1))
        return min(matches)


    # keeps track of costs of a word and how far to backtrack to find the start of the word
    costs_by_idx = [(0, 0)] # (word cost, length of word)
    for i in range(1, len(s) + 1):
        lowest_cost_by_idx = lowest_cost(i)
        costs_by_idx.append(lowest_cost_by_idx)

    # segment the input string based on lowest cost starting from the end of the costs array
    words = []
    i = len(s)
    while i > 0:
        backtrack = costs_by_idx[i][1]
        words.append(s[i - backtrack:i])
        i -= backtrack
    return reversed(words)

if __name__ == '__main__':
    test_words = ["ashwednesday", "outerbanksnetflix", "sarahcameron", "rollingupthewelcomemat", "elementsofstatisticallearning", "yourmissionshouldyouchoosetoacceptit", "thismessagewillselfdestructinfiveseconds"]
    for test_word in test_words:
        output = segment(test_word)
        print("{} --> {}".format(test_word, " ".join(output)))
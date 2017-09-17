import sys

def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    return words


def sort_words(words):
    counted_words = {}
    for i in range(len(words)):
        if counted_words.get(words[i]) is None:
            counted_words[words[i]] = 1
        else:
            counted_words[words[i]] += 1

    return counted_words


def print_words(sorted_words):
    alphabet_sort = sorted(sorted_words.items())
    print(alphabet_sort)


def print_top(sorted_words):
    freq_sort = sorted(sorted_words.items(), key=lambda x:x[1], reverse=True)
    print(freq_sort[:20])

if __name__ = "__main__":
    filename = input("enter file name: ")
    words = read_words(filename)
    sorted_words = sort_words(words)
    print_words(sorted_words)
    print_top(sorted_words)



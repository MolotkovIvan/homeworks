import sys

def read_words(filename):
    words = []
    with open(filename, "r") as f:
        for line in f:
            words.extend(line.split())
    for i in range(len(words)):
        words[i].lower()    
    return words


def sort_words(words):
    counted_words = {}
    for word in words:
        word = word.lower()        
        if word not in counted_words:
            counted_words[word] = 1
        else:
            counted_words[word] += 1

    return counted_words


def print_words(sorted_words):
    alphabet_sort = sorted(sorted_words.items())
    for a,b in alphabet_sort:
        print(a, b)

def print_top(sorted_words):
    freq_sort = sorted(sorted_words.items(), key=lambda x:x[1], reverse=True)
    for a,b in freq_sort:
        print(a, b)
if __name__ = "__main__":
#if True:
    filename = input("enter file name: ")
    words = read_words(filename)
    sorted_words = sort_words(words)
    print_words(sorted_words)
    print_top(sorted_words)



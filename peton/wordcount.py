def sort_words(file):
    with open(file, "r") as f:
        counted_words = {}
        for line in f:
            s = line.lower()
            i = 0
            while i < len(s):
                if ((ord(s[i]) <= ord('z') and ord(s[i]) >= ord('a')) or s[i] == " ") == False:
                    s = s[:i] + s[i+1:]
                    i-=1
                i+=1
            all_words = s.split()
            for i in range(len(all_words)):
                if counted_words.get(all_words[i]) is None:
                    counted_words[all_words[i]] = 1
                else:
                    counted_words[all_words[i]] += 1

    return counted_words


def print_words(file):
    alphabet_sort = sorted(sort_words(file).items())
    return alphabet_sort


def print_top(file):
    freq_sort = sorted(sort_words(file).items(), key=lambda x:x[1], reverse=True)
    if len(freq_sort) > 20:
        return freq_sort[:20]
    return freq_sort


print(print_words("textful"))
print(print_top("textful"))




def verbing(s):
    if len(s) < 3:
        return s
    if s[-3:] == "ing":
        return s + "ly"
    return s + "ing"


def not_bad(s):
    not_loc = s.find("not")
    bad_loc = s.find("bad")
    
    if (not_loc != -1 and bad_loc != -1) and (not_loc < bad_loc):
        return s[:not_loc] + "good" + s[bad_loc+3:]


def front_back(a,b):
    len_a = (len(a)+1)//2
    len_b = (len(b)+1)//2    
    return a[:len_a] + b[:len_b] + a[len_a:] + b[len_b:]


#if True:
if __name__ = "__main__":
    print(verbing(input()))
    print(not_bad(input()))
    print(front_back(input(), input()))

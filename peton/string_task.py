def verbing(s):
    if len(s) < 3:
        return s
    if s[-3:] == "ing":
        return s + "ly"
    return s + "ing"


def not_bad(s):
    if (s.find("not") != -1 and s.find("bad") != -1) and (s.find("not") < s.find("bad")):
        return s[:s.find("not")] + "good" + s[s.find("bad")+3:]


def front_back(a,b):
    return a[:(len(a) + 1)//2] + b[:(len(b) + 1)//2] + a[(len(a) + 1)//2:] + b[(len(b) + 1)//2:]




print(verbing(input()))
print(not_bad(input()))
print(front_back(input(), input()))
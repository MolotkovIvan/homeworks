def remove_adjacent(lst):
    return [lst[i] for i in range(len(lst)) if i == len(lst)-1 or lst[i] != lst[i+1]]


def linear_merge(lst1, lst2):
    i = 0
    j = 0
    merged = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            merged.append(lst1[i])
            i+=1
        else:
            merged.append(lst2[j])
            j+=1

    return merged + lst1[i:] + lst2[j:]

if __name__ = "__main__":
#if True:
    s = input("Enter the sequence to be apllied remove_adjacent() to: ").split()
    lst = []
    for i in range(len(s)):
        lst.append(int(s[i]))
    lst = remove_adjacent(lst)

    q1 = input("Enter the first sequence to be apllied linear_merge() to: ").split()
    q2 = input("Enter the second sequence to be apllied linear_merge() to: ").split()
    lst1 = []
    lst2 = []
    for i in range(len(q1)):
        lst1.append(int(q1[i]))
    for i in range(len(q2)):
        lst2.append(int(q2[i]))
    answer = linear_merge(lst1, lst2)

    print("rip equal adjacent items ", lst)
    print("two arrays were merged into this: ", answer)

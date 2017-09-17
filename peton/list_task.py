def remove_adjacent(lst):
    i = 0
    while i < (len(lst)-1):
        if lst[i] == lst[i+1]:
            lst.pop(i+1)
            i -= 1
        i+=1
    return lst


def linear_merge(lst1, lst2):
    i = 0
    j = 0
    merged = []
    while i < len(lst1) and j < len(lst2):
        if j < len(lst2) and i < len(lst1):
            if lst1[i] < lst2[j]:
                merged.append(lst1[i])
                i+=1
            else:
                merged.append(lst2[j])
                j+=1

    while i < len(lst1):
        merged.append(lst1[i])
        i+=1
    while j < len(lst2):
        merged.append(lst2[j])
        j+=1

    return merged

if __name__ = "__main__":
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

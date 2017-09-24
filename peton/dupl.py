import os
import sys
from hashlib import sha1 as hasher


def hashing(file_path):
    h = hasher()
    f1 = open(file_path, 'rb')
    h.update(f1.read())
    return h.hexdigest()    


def eq_files(catalog):
    global all_files    
    lst = os.listdir(catalog)    
    for i in lst:
        full_path = os.path.join(catalog, i)        
        if os.path.isfile(full_path):
            code = hashing(full_path)            
            if code not in all_files:
                all_files[code] = [1, [i], [catalog[len(start_path)+1:]]]                
            else:
                all_files[code][0] += 1;
                all_files[code][1].append(i)                
                all_files[code][2].append(catalog[len(start_path)+1:])
        elif os.path.isdir(full_path):
            eq_files(full_path)
    

all_files = {}
start_path = input("enter top_dir ")
eq_files(start_path)
for a in all_files.items():
    if a[1][0] > 1:
        for i in range(a[1][0]-1):
            if (a[1][2][i] == ''):
                print(a[1][1][i], end=":")
            else:
                print(a[1][2][i] + "/" + a[1][1][i], end=":")
        
        if (a[1][2][a[1][0]-1] == ''):
            print(a[1][1][a[1][0]-1])
        else:
            print(a[1][2][a[1][0]-1] + "/" + a[1][1][a[1][0]-1])
                                
        print()    

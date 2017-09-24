import timeit
import os
import sys
from hashlib import sha1 as hasher


def hashing(file_path):
    text = "~"    
    with open(file_path, mode='rb') as f:        
        h = hasher()
        while text != "":
            text = f.read(2**10)        
            h.update(text)
            return h.hexdigest()    


def eq_files(catalog):
    all_files = {}
    for root, _, files in os.walk(catalog):
        for i in files:
            full_path = os.path.join(root,i);
            code = hashing(full_path)            
            if code not in all_files:
                all_files[code] = [os.path.relpath(full_path, start_path)]                
            else:
                all_files[code].append(os.path.relpath(full_path, start_path))
    return all_files


if __name__ == "__main__":
    start_path = sys.argv[1]
    for a in  eq_files(start_path).values():
        if len(a) > 1:
            print(":".join(a))
#    print(timeit.timeit("eq_files(sys.argv[1])", setup="from __main__ import eq_files", number=1))

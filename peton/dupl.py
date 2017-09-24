import os
import sys
from hashlib import sha1 as hasher


def hashing(file_path):
    with open(file_path, mode='rb') as f:        
        h = hasher()
        h.update(f.read())
        return h.hexdigest()    


def eq_files(catalog):
    global all_files    
    for root, dirs, files in os.walk(catalog):
        for i in files:
            full_path = os.path.join(root,i);
            code = hashing(full_path)            
            if code not in all_files:
                all_files[code] = [full_path[len(start_path)+1:]]                
            else:
                all_files[code].append(full_path[len(start_path)+1:])
if __name__ == "__main__":
#if True:
    all_files = {}
#    start_path = "/home/ivanmolotkov/Документы/lab02"    
    start_path = input("enter top_dir ")
    eq_files(start_path)
    for a in all_files.items():
        if len(a[1]) > 1:
            print(":".join(tuple(a[1])))

import os
import sys
from hashlib import sha1 as hasher


def hashing(file_path):
    while True:    
        with open(file_path, mode='rb') as f:        
            h = hasher()
            h.update(f.read(2**15))
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
#    start_path = "/home/ivanmolotkov/Документы/lab02"    
    start_path = sys.argv[1]
    for a in  eq_files(start_path).values():
        if len(a) > 1:
            print(":".join(a))

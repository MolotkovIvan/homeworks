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
    for _, dirs, files in os.walk(catalog):
        if (files[0] == "." or files[0] == "~"):
            continue        
        full_path = os.path.join(dirs, files)        
        code = hashing(full_path)            
        if code not in all_files:
            all_files[code] = [full_path]                
        else:
            all_files[code].append(full_path)
    
if __name__ == "__main__":
#if True:
    all_files = {}
    start_path = input("enter top_dir ")
    eq_files(start_path)
    for a in all_files.items():
        if len(a[1]) > 1:
            for i in range(len(a[1])):
                print(":".join(a[1]))             


#!/usr/bin/env python3

import os
import time

''' Limited to one (1) snapshot file at the moment. '''

snapshot_file = "./snapshot.txt"

def homer(out_root, out_source, in_root):
    if out_source.find(out_root) is not 0:
        return None
    pos = len(out_root)
    return in_root + out_source[pos:] 

def get_dir(prompt, times = 4):
    ztimes = 0
    while ztimes < times:
        zroot = input(prompt)
        if os.path.isdir(zroot):
            return zroot
        ztimes += 1
        print('Directory "{}" not found'.format(zroot))
    return None

def do_snapshot():
    zroot = get_dir("Enter snapshot source: ")
    if not zroot:
        print("Operation aborted.")
        return
    print("Writing " + snapshot_file + '...')
    nelem = 0
    with open(snapshot_file, 'w') as fh:
        print(zroot, time.time(), sep='\t', file=fh)
        for droot, zdirs, zfiles in os.walk(zroot):
            for node in zfiles:
                zfile = os.path.join(droot, node)
                zstat = os.stat(zfile, follow_symlinks=False)
                print(zfile, zstat.st_mtime, sep='\t', file=fh)
                nelem += 1
    print("Created ",snapshot_file,", found", nelem, "files.")

def do_apply():
    with open(snapshot_file) as fh:
        line = fh.readline().split('\t')
        archive_root = line[0]
        print("Snapshot:", archive_root)
        zroot = get_dir("Enter destination: ")
        if not zroot:
            print("Operation aborted.")
            return
        nelem = 0
        for line in fh.readlines():
            line = line.split('\t')
            effective = homer(archive_root, line[0], zroot)
            if not effective:
                print("Skipping", line[0])
                continue
            try:
                zhack = float(line[1])
                os.utime(effective, times=(zhack, zhack))
                # print(effective)
                nelem += 1
            except Exception as ex:
                #print(effective, ex)
                pass
        print("Touched", nelem, "files.")

def do_delete():
    if not os.path.exists(snapshot_file):
        return
    zyes = input("Enter 'yes' to delete shapshot file: ")
    if zyes.lower() == 'yes':
        os.unlink(snapshot_file)
        if not os.path.exists(snapshot_file):
            print("Shapshot file deleted.")
        else:
            print("Unable to remove " + shapshot_file)

opts = (
    (1, "Create Snapshot", do_snapshot),
    (2, "Apply  Snapshot", do_apply),
    (3, "Delete Snapshot", do_delete),
    (4, "Quit", quit)
    )

choice = 0
while choice is not 3:
    for opt in opts:
        print(opt[0], opt[1])
    zchoice = input("Choice: ")
    try:
        choice = int(zchoice)
        choice -= 1
    except:
        print("Invalid choice. Try again.")
        continue
    if choice >= 0 and choice < len(opts):
        which = opts[choice]
        which[2]()
    else:
        print("Choice out of range. Try again.")
    


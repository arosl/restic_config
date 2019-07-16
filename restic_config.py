#!/usr/bin/env python3
'''
Generate a restic config for MacOS in
~.config/restic/
'''
import subprocess
import plistlib
import os

def get_plist_dict(path):
    fn = path
    if not os.path.exists(fn):
        return None
    with open(fn, 'rb') as f:
        pl = plistlib.load(f)
    return pl


#MacOS backup standard exclusions file
stdexclusions = get_plist_dict('/System/Library/CoreServices/backupd.bundle/Contents/Resources/StdExclusions.plist')

user_dir = os.path.expanduser('~')
restic_confdir = os.path.expanduser('~/.config/restic/')
excl_restic = os.path.join(restic_confdir + "exclusions")

#Create config dir
if not os.path.exists(restic_confdir):
    os.makedirs(restic_confdir)

#find all files with com_apple_backup_excludeItem set
mdfind = subprocess.run(['sudo', 'mdfind', "com_apple_backup_excludeItem = 'com.apple.backupd'"], capture_output=True, text=True)

#Write restic exclution file
with open(excl_restic, 'w') as f:
    print('# MacOS standard paths excluded', file=f)
    for line in stdexclusions['PathsExcluded']:
        print(line, file=f)
    print('\n# MacOS user paths excluded', file=f)
    for line in stdexclusions['UserPathsExcluded']:
        print(user_dir + '/' + line, file=f)   
    print('\n# MacOS paths where content should be excluded', file=f)
    for line in stdexclusions['ContentsExcluded']:
        print(line + '/*', file=f)    
    print('\n# MacOS paths where file content should be excluded', file=f)
    for line in stdexclusions['FileContentsExcluded']:
        print(line + '/*', file=f)    
    print('\n# mdfind com_apple_backup_excludeItem', file=f)
    print(mdfind.stdout, file=f)
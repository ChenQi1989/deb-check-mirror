#!/usr/bin/python3
#
# deb-check.py
#

import sys
import os
import subprocess

def get_pkg_mirror(pkg):
    """
    Return the mirror for pkg
    """
    output = subprocess.check_output(f"apt-cache policy {pkg}", shell=True).decode('utf-8')
    lines = output.split('\n')
    got_version_table = False
    priority_used = None
    for line in lines:
        line = line.strip()
        if line.startswith('***'):
            got_version_table = True
            priority_used = line.split()[-1]
            continue
        if not got_version_table:
            continue
        # we get here after version table
        comps_line = line.split()
        priority = comps_line[0]
        mirror = comps_line[1]
        if priority == priority_used:
            return mirror
    return None

def main():
    # A dict of {pkg:mirror} to store final results
    pkg_mirror = {}
    
    # apt update
    dropped = subprocess.check_output('apt update', stderr=subprocess.STDOUT, shell=True)
    output = subprocess.check_output('dpkg -l | grep ^ii', shell=True).decode('utf-8')

    # get installed packages
    inst_pkgs = []
    for line in output.split('\n'):
        line = line.strip()
        if not line:
            continue
        pkg = line.split()[1]
        #print(pkg)
        inst_pkgs.append(pkg)

    # get the mirror information
    for pkg in inst_pkgs:
        mirror = get_pkg_mirror(pkg)
        if not mirror:
            print(f"Failed to get mirror for {pkg}")
            sys.exit(1)
        pkg_mirror[pkg] = mirror
        print(f"{pkg}: {mirror}")


if __name__ == "__main__":
    try:
        ret = main()
    except Exception:
        ret = 1
        import traceback
        traceback.print_exc()
    sys.exit(ret)


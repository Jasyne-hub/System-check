#!/usr/bin/env python3

#---Overall Goal of this Script---
#The aim of this script is to gather system information and log it
#Specifically, the current processes that are being run by the user
#The current Memory usage
#And the Current Disk space
#Each of which would be logged to a file named system_check.logs

import subprocess
import sys
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
LOG_FILE = os.path.join(BASE_DIR, "system_check.log")

def getProcessInfo():
    """
    This function gathers information on the processes being run by only the user and prints it out
    """
    try:
        username = subprocess.run(["whoami"], capture_output=True, text=True, check=True).stdout.strip()
        cmd = f'echo "PID CPU MEM PROCESS" && ps aux | grep [{username[0]}]{username[1:]} | grep -v -- --type=renderer | awk \'{{print $2, $3, $4, $11}}\''
        result = subprocess.run(
            cmd, 
            shell=True,
            capture_output=True,
            text=True,
            check=True
            )
        
        print(f"The processes currently being run by {username} are:")
        print("\n")
        print(result.stdout)

        return result.stdout
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

def getStorStat():
    """
    This function gathers information about storage space on the system including Total space, Used space and Available space
    """
    try: 
        storage_stat = subprocess.run(
            ["df", "-h"], 
            capture_output=True, 
            text=True, 
            check=True
            )
        
        row = storage_stat.stdout.splitlines()[2].split()
        used = row[2]
        avail = row[3]
        total = row[1]

        print(f"---STORAGE STATISTICS---")
        print(f"Total: {total}")
        print(f"Used: {used}")
        print(f"Available: {avail}")
        print("\n")

        data = f"---STORAGE STATISTICS--- \n Total: {total} \n Used: {used} \n Available: {avail}"

        return data
    
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

def getMemStat():
    """
    This function gathers information about the memory, including the Total memory, Used memory and Available memory
    """
    try:
        mem_stat = subprocess.run(
            ["free", "-h"], 
            capture_output=True, 
            text=True, 
            check=True
            )
        
        mem_row = mem_stat.stdout.splitlines()[1].split()
        total_mem = mem_row[1]
        used_mem = mem_row[2]
        free_mem = mem_row[6]
        swap_row = mem_stat.stdout.splitlines()[2].split()
        total_swap = swap_row[1]
        used_swap = swap_row[2]
        free_swap = swap_row[3]

        print(f"---MEMORY STATISTICS---")
        print(f"Total: {total_mem}")
        print(f"Used: {used_mem}")
        print(f"Available: {free_mem}")
        print(f"---For Memory Overload(Swapping)---")
        print(f"Total: {total_swap}")
        print(f"Used: {used_swap}")
        print(f"Available: {free_swap}")
        print("\n")

        data = f"---MEMORY STATISTICS--- \n Total: {total_mem} \n Used: {used_mem} \n Available: {free_mem} \n ---For Memory Overload(Swapping)--- \n Total: {total_swap} \n Used: {used_swap} \n Available: {free_swap}"

        return data 
    except subprocess.CalledProcessError as e:
        print(f"Error executing command: {e}")
        print(f"Stderr: {e.stderr}")
        sys.exit(1)

def logResult(cpu_info, storage_info, memory_info):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, 'a') as f:
        f.write(f"--- {now} -----------------------------------------------------------------------------------------------------\n\n")
        f.write(f"{cpu_info}\n\n")
        f.write(f"{memory_info}\n\n")
        f.write(f"{storage_info}\n\n")
    print(f"Successfully logged to {LOG_FILE}")


def main():
    print("Running the System Check Script Now... \n")
    proc_info = getProcessInfo()
    mem_info = getMemStat()
    stor_info = getStorStat()
    logResult(proc_info, stor_info, mem_info)

if __name__ == '__main__':
    main()

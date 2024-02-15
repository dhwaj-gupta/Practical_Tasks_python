#!/bin/usr/python3
#Get all the important dependencies
import subprocess
import sys
import platform
import psutil
import socket
#Function to display distro info
def get_distro_info():
    return platform.mac_ver()
#Function to display memory info
def get_memory_info():
    mem = psutil.virtual_memory()
    total = mem.total
    used = mem.used
    free = mem.free
    return total, used, free
#Function to display cpu info
def get_cpu_info():
    cpu_info = {
        'model': platform.processor(),
        'core_count': psutil.cpu_count(logical=False),
        'speed': psutil.cpu_freq().current
    }
    return cpu_info
#Function to display user info
def get_user_info():
    return platform.node()
#Function to display load average
def get_load_average():
    return psutil.getloadavg()
#Function to display ip address
def get_ip_address():
    result = subprocess.run(['ifconfig'], capture_output=True, text=True)
    output = result.stdout
    lines = output.split('\n')
    for line in lines:
        if 'inet ' in line:
            parts = line.split()
            ip_address = parts[1]
            if ip_address != '127.0.0.1':  # Exclude loopback address
                return ip_address
    return None
#Main function where all the information is displayed according to command line arguments
def main():
    if len(sys.argv) < 2:
        print("Usage: python script_name.py [-d] [-m] [-c] [-u] [-l] [-i]")
        sys.exit(1)

    for arg in sys.argv[1:]:
        if arg == "-d":
            print("Distro Info:", get_distro_info())
        elif arg == "-m":
            total, used, free = get_memory_info()
            print("Memory Info:")
            print(f"Total Memory: {total} bytes")
            print(f"Used Memory: {used} bytes")
            print(f"Free Memory: {free} bytes")
        elif arg == "-c":
            cpu_info = get_cpu_info()
            print("CPU Info:")
            print(f"Model: {cpu_info['model']}")
            print(f"Core Count: {cpu_info['core_count']}")
            print(f"Speed: {cpu_info['speed']} MHz")
        elif arg == "-u":
            print("User Info:", get_user_info())
        elif arg == "-l":
            print("Load Average:", get_load_average())
        elif arg == "-i":
            print("IP Address:", get_ip_address())
        else:
            print(f"Invalid argument: {arg}")

if __name__ == "__main__":
    main()


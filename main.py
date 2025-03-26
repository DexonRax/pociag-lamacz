import os
import re
import json

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    WHITE ='\033[0;37m'  


def main():
    print(r"""
______ _____ _____ _____  ___  _____    _       ___  ___  ___  ___  _____  ______   _   _  __     _____ 
| ___ \  _  /  __ \_   _|/ _ \|  __ \  | |     / _ \ |  \/  | / _ \/  __ \|___  /  | | | |/  |   |  _  |
| |_/ / | | | /  \/ | | / /_\ \ |  \/  | |    / /_\ \| .  . |/ /_\ \ /  \/   / /   | | | |`| |   | |/' |
|  __/| | | | |     | | |  _  | | __   | |    |  _  || |\/| ||  _  | |      / /    | | | | | |   |  /| |
| |   \ \_/ / \__/\_| |_| | | | |_\ \  | |____| | | || |  | || | | | \__/\./ /___  \ \_/ /_| |_ _\ |_/ /
\_|    \___/ \____/\___/\_| |_/\____/  \_____/\_| |_/\_|  |_/\_| |_/\____/\_____/   \___/ \___/(_)\___/                                                                                                     
    """)

#--script=s7-ifo
#--script=modbus_discovery

    network_device = "eth0"
    nmap_command = "sudo nmap -T3 --script vuln -O -A -sS -p 22,23,80,443,502,102,20000,2404,47808,4840 $(ip a | grep eth0 | awk '{print $2}' | tail -n 1)"
    output = os.popen(nmap_command).read()
    #print(output)
    ports = []
    addres_number = -1

    mac_address = ""
    text = "network_deivce: " + network_device + "\n"
    nmap_log_file = open("nmap.log", "w")
    nmap_log_file.write(output)
    nmap_log_file.close()

    for line in output.split("\n"):

        if "Nmap scan report for" in line:
            ports.append([])
            addres_number += 1
            ports[addres_number].append(line.split(" ")[4])

        if "open" in line and "Warning" not in line:
            ports[addres_number].append(re.split(r'[;,\s]+', line))
        elif "filtered" in line and "Warning" not in line:
            ports[addres_number].append(re.split(r'[;,\s]+', line))
        elif "closed" in line and "Warning" not in line:
            ports[addres_number].append(re.split(r'[;,\s]+', line))

        if "MAC Address:" in line:
            mac_address = line.split(" ")[2]

        if "Nmap done:" in line:
            print(line)

    print("scanned addresses: ", addres_number+1, "\n")
    for i in range(addres_number+1):
        for port in ports[i]:
            if port == ports[i][0]:
                print(bcolors.WHITE + bcolors.BOLD + "IP: " + port + bcolors.WHITE)
            if port[1] == "open":
                print(bcolors.OKGREEN + port[0].split("/")[0] + " [" + port[0].split("/")[1] + "] ("+ port[2] +")")
            if port[1] == "filtered":
                print(bcolors.WARNING + port[0].split("/")[0] + " [" + port[0].split("/")[1] + "] ("+ port[2] +")")
            if port[1] == "closed":
                print(bcolors.FAIL + port[0].split("/")[0] + " [" + port[0].split("/")[1] + "] ("+ port[2] +")")
                
        print("\n" + bcolors.WHITE)
    print(bcolors.BOLD + bcolors.OKCYAN + "MAC: " + mac_address)

    nmap_log_clean_file = open("nmapclean.log", "w")


    nmap_log_clean_file.write(json.dumps(ports))
    nmap_log_clean_file.close()
    
if __name__ == "__main__":
    main()
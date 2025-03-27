import subprocess, xmltodict, json, re
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
def discoverHosts(subnet):
    cmd = f"sudo nmap -sn {subnet} -oX hosts.xml"
    subprocess.run(cmd, shell=True)

    with open("hosts.xml", "r") as file:
        xml_data = file.read()

    import xmltodict
    data = xmltodict.parse(xml_data)
    
    hosts = []
    for host in data['nmaprun']['host']:
        if 'address' in host:
            ip = host['address']['@addr']
            hosts.append(ip)

    return hosts
def main():
    print(r"""
______ _____ _____ _____  ___  _____    _       ___  ___  ___  ___  _____  ______   _   _  __     _____ 
| ___ \  _  /  __ \_   _|/ _ \|  __ \  | |     / _ \ |  \/  | / _ \/  __ \|___  /  | | | |/  |   |  _  |
| |_/ / | | | /  \/ | | / /_\ \ |  \/  | |    / /_\ \| .  . |/ /_\ \ /  \/   / /   | | | |`| |   | |/' |
|  __/| | | | |     | | |  _  | | __   | |    |  _  || |\/| ||  _  | |      / /    | | | | | |   |  /| |
| |   \ \_/ / \__/\_| |_| | | | |_\ \  | |____| | | || |  | || | | | \__/\./ /___  \ \_/ /_| |_ _\ |_/ /
\_|    \___/ \____/\___/\_| |_/\____/  \_____/\_| |_/\_|  |_/\_| |_/\____/\_____/   \___/ \___/(_)\___/                                                                                                     
    """)

    network_device = "eth0"
    nmap_cmd = "sudo nmap -sn -T3 --script vuln -A -sS -p 22,23,80,443,502,102,20000,2404,47808,4840 -oX log.xml $(ip a | grep " + network_device + " | awk '{print $2}' | tail -n 1)"
    output = subprocess.run(nmap_cmd, shell=True, capture_output=True, text=True).stdout
    with open("log.xml") as xml_file, open("log.json", "w") as json_file:
        json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)

    ports = []
    addres_number = -1
    mac_address = ""

    subnet = input("Enter subnet with mask (e.g., 192.168.1.0/24): ").strip()
    hosts = discoverHosts(subnet)
    print("\nFound hosts: ", hosts)
    
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
    
if __name__ == "__main__":
    main()
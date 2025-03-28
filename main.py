import subprocess, xmltodict, json, os, shutil

if os.path.exists("logs"):
    shutil.rmtree("logs")

class bcolors:
    OKGREEN = '\033[92m'  # Zielony dla otwartych
    WARNING = '\033[93m'  # Żółty dla filtrowanych
    FAIL = '\033[91m'     # Czerwony dla zamkniętych
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def scan_active_hosts(subnet, range_start, range_end):

    cmd = f"sudo nmap -sn {subnet}.{range_start}-{range_end} -oX logs/hosts.xml"
    subprocess.run(cmd, shell=True)

    with open("logs/hosts.xml", "r") as file:
        data = xmltodict.parse(file.read())
    
    hosts = []
    if 'host' in data['nmaprun']:
        host_data = data['nmaprun']['host']
        if isinstance(host_data, list):
            for host in host_data:
                addresses = host['address']
                if isinstance(addresses, list):
                    for addr in addresses:
                        if addr['@addrtype'] == 'ipv4':
                            hosts.append(addr['@addr'])
                elif addresses['@addrtype'] == 'ipv4':
                    hosts.append(addresses['@addr'])
        elif isinstance(host_data, dict):
            addresses = host_data['address']
            if isinstance(addresses, list):
                for addr in addresses:
                    if addr['@addrtype'] == 'ipv4':
                        hosts.append(addr['@addr'])
            elif addresses['@addrtype'] == 'ipv4':
                hosts.append(addresses['@addr'])

    if not hosts:
        print("Brak aktywnych hostów.")
        return {}
    print("\nScanning resources....")
    
    results = {}
    for ip in hosts:
        cmd = f"sudo nmap -T4 -sS -A -p 22,23,80,443,502,5020,102,20000,2404,47808,4840 -oX logs/resources.xml {ip}"
        subprocess.run(cmd, shell=True, capture_output=True, text=True)

        with open("logs/resources.xml", "r") as file:
            data = xmltodict.parse(file.read())

        details = {"ports": [], "os": None}
        if 'host' in data['nmaprun']:
            host = data['nmaprun']['host']
            if isinstance(host, list):
                host = host[0]

            if 'ports' in host and 'port' in host['ports']:
                ports = host['ports']['port']
                if isinstance(ports, list):
                    for port in ports:
                        port_id = port['@portid']
                        state = port['state']['@state']
                        service = port.get('service', {}).get('@name', 'unknown')
                        details["ports"].append({"port": port_id, "state": state, "service": service})
                elif isinstance(ports, dict):
                    port_id = ports['@portid']
                    state = ports['state']['@state']
                    service = ports.get('service', {}).get('@name', 'unknown')
                    details["ports"].append({"port": port_id, "state": state, "service": service})

            if 'os' in host and 'osmatch' in host['os']:
                osmatch = host['os']['osmatch']
                details["os"] = osmatch['@name'] if isinstance(osmatch, dict) else osmatch[0]['@name']

        results[ip] = details

    return results

def scan_modbus(subnet, range_start, range_end):
    cmd = f"sudo nmap -p 502 --script modbus-discover {subnet}.{range_start}-{range_end} -oX logs/modbus.xml"
    output = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout
    print("Wynik skanowania Modbus:\n", output)

def main():
    print(r"""
______ _____ _____ _____  ___  _____    _       ___  ___  ___  ___  _____  ______   _   _  __     _____ 
| ___ \  _  /  __ \_   _|/ _ \|  __ \  | |     / _ \ |  \/  | / _ \/  __ \|___  /  | | | |/  |   |  _  |
| |_/ / | | | /  \/ | | / /_\ \ |  \/  | |    / /_\ \| .  . |/ /_\ \ /  \/   / /   | | | |`| |   | |/' |
|  __/| | | | |     | | |  _  | | __   | |    |  _  || |\/| ||  _  | |      / /    | | | | | |   |  /| |
| |   \ \_/ / \__/\_| |_| | | | |_\ \  | |____| | | || |  | || | | | \__/\./ /___  \ \_/ /_| |_ _\ |_/ /
\_|    \___/ \____/\___/\_| |_/\____/  \_____/\_| |_/\_|  |_/\_| |_/\____/\_____/   \___/ \___/(_)\___/                                                                                                     
    """)

    print("0. Find active hosts and their resources in the subnet")
    print("1. Check modbus for vulnerabilities")

    answer = input("Choose option: ")

    subnet = input("Enter subnet (e.g., 10.0.2): ").strip()
    range_start = input("Enter first address (e.g., 1): ").strip()
    range_end = input("Enter last address (e.g., 18): ").strip()

    os.makedirs("logs", exist_ok=True)
    
    if answer == "0":
        results = scan_active_hosts(subnet, range_start, range_end)

        for ip, details in results.items():
            print(f"\n{bcolors.BOLD}Host: {ip}{bcolors.ENDC}")
            for port in details['ports']:
                if port['state'] == 'open':
                    color = bcolors.OKGREEN
                elif port['state'] == 'filtered':
                    color = bcolors.WARNING
                else: 
                    color = bcolors.FAIL
                print(f"{color}Port {port['port']}: {port['state']} ({port['service']}){bcolors.ENDC}")
            if details['os']:
                print(f"System operacyjny: {details['os']}")

    elif answer == "1":
        scan_modbus(subnet, range_start, range_end)

    try:
        with open("logs/hosts.xml") as xml_file, open("logs/hosts.json", "w") as json_file:
            json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        with open("logs/resources.xml") as xml_file, open("logs/resources.json", "w") as json_file:
            json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        if os.path.exists("logs/modbus.xml"):
            with open("logs/modbus.xml") as xml_file, open("logs/modbus.json", "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
    except Exception as e:
        print(f"{bcolors.FAIL}Error while converting XML to JSON: {e}{bcolors.ENDC}")

if __name__ == "__main__":
    main()
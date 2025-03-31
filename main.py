import subprocess, xmltodict, json, os, shutil, argparse

class bcolors:
    OKGREEN = '\033[92m' 
    WARNING = '\033[93m' 
    BGTEXT = '\033[90m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UDLN = '\033[4m'
    

if os.path.exists("logs"):
    shutil.rmtree("logs")
    print(f"{bcolors.OKGREEN}Deleted existing log files.{bcolors.ENDC}")

def scan_active_hosts(subnet, range_start, range_end, nmap_flags, nmap_ports):
    print(f"{bcolors.BGTEXT}\nPerforming hosts scan...{bcolors.ENDC}")
    cmd = f"sudo nmap -sn {subnet}.{range_start}-{range_end} -oX logs/hosts.xml"
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    process.wait()

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
        print(f"{bcolors.WARNING}No active hosts.{bcolors.ENDC}")
        return {}
    print("\nScanning resources....")
    
    results = {}
    for ip in hosts:
        cmd = f"sudo nmap {nmap_flags} -p {nmap_ports} -oX logs/resources.xml {ip}"
        print(f"Executing: {cmd}")
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

def scan_modbus(subnet, range_start, range_end, nmap_flags):
    print(f"\n{bcolors.BGTEXT}Performing modbus scan...{bcolors.ENDC}")
    cmd = f"sudo nmap {nmap_flags} -p 502 --script modbus-discover {subnet}.{range_start}-{range_end} -oX logs/modbus.xml"
    print(f"{bcolors.BGTEXT}Executing: {cmd}{bcolors.ENDC}")
    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    output = process.communicate()[0]
    print(f"{bcolors.BOLD}Modbus scan results:\n{bcolors.ENDC}", output)

def scan_vurnabilities(subnet, range_start, range_end, nmap_flags, nmap_ports, nmap_vurnability_script):
    print(f"\n{bcolors.BGTEXT}Performing vulnerability scan...{bcolors.ENDC}")
    cmd_vuln = f"sudo nmap {nmap_flags} -p {nmap_ports} --script {nmap_vurnability_script} {subnet}.{range_start}-{range_end} -oX logs/vulnerabilities.xml"
    print(f"{bcolors.BGTEXT}Executing: {cmd_vuln}{bcolors.ENDC}") 
    process = subprocess.Popen(cmd_vuln, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    vuln_output = process.communicate()[0]
    print("Vulnerability scan results:\n", vuln_output)

def main():
    parser = argparse.ArgumentParser(description="Network scanning tool with Nmap")
    parser.add_argument("-s", "--subnet", help="Subnet to scan (e.g., 10.0.2)")
    parser.add_argument("-r", "--range", nargs=2, metavar=('start', 'end'), help="Range of addresses (e.g., 1 18)")
    parser.add_argument("-o", "--option", choices=['0', '1', '2'], help="Scan option: 0=hosts+resources, 1=vulnerabilities, 2=modbus")
    parser.add_argument("-p", "--ports", default="22,23,80,443,502,5020,102,20000,2404,47808,4840", 
                        help="Nmap ports, comma-separated, in quotation marks (default: 22,23,80,443,502,5020,102,20000,2404,47808,4840)")
    parser.add_argument("-f", "--flags", default="-T4 -sS -A", 
                        help="Nmap flags, space-separated, in quotation marks (default: -T4 -sS -A)")
    parser.add_argument("-v", "--vuln-script", default="default", 
                        help="Nmap vulnerability script (default: default)")

    args = parser.parse_args()
    
    print(r"""
______ _____ _____ _____  ___  _____    _       ___  ___  ___  ___  _____  ______   _   _  __     _____ 
| ___ \  _  /  __ \_   _|/ _ \|  __ \  | |     / _ \ |  \/  | / _ \/  __ \|___  /  | | | |/  |   |  _  |
| |_/ / | | | /  \/ | | / /_\ \ |  \/  | |    / /_\ \| .  . |/ /_\ \ /  \/   / /   | | | |`| |   | |/' |
|  __/| | | | |     | | |  _  | | __   | |    |  _  || |\/| ||  _  | |      / /    | | | | | |   |  /| |
| |   \ \_/ / \__/\_| |_| | | | |_\ \  | |____| | | || |  | || | | | \__/\./ /___  \ \_/ /_| |_ _\ |_/ /
\_|    \___/ \____/\___/\_| |_/\____/  \_____/\_| |_/\_|  |_/\_| |_/\____/\_____/   \___/ \___/(_)\___/                                                                                                     
    """)
    print(f"{bcolors.BOLD}Default flags, ports, scripts can be changed via command-line arguments or below at scan variables{bcolors.ENDC}")

    if args.subnet and args.range and args.option:
        subnet = args.subnet
        range_start = args.range[0]
        range_end = args.range[1]
        answer = args.option
        nmap_ports = args.ports
        nmap_flags = args.flags
        nmap_vurnability_script = args.vuln_script
        print(f"{bcolors.BGTEXT}Debug: subnet={subnet}, range_start={range_start}, range_end={range_end}, option={answer}")
        print(f"Debug: ports={nmap_ports}, flags={nmap_flags}, vuln_script={nmap_vurnability_script}{bcolors.ENDC}")
    else:
        print("  0. Find active hosts and their resources in the subnet")
        print("  1. Find active hosts, their resources and vulnerabilities in the subnet")
        print("  2. Check modbus for vulnerabilities (should work only with an activated modbus)")
        answer = input("Choose option: ").strip()
        if not answer or answer not in ['0', '1', '2']:
            print(f"{bcolors.FAIL}Invalid option selected. Please choose 0, 1, or 2.{bcolors.ENDC}")
            return
        subnet = input(f"{bcolors.UDLN}Enter subnet (e.g., 10.0.2): ").strip()
        range_start = input("Enter first address (e.g., 1): ").strip()
        range_end = input(f"Enter last address (e.g., 18): {bcolors.ENDC}").strip()

        # Scan variables (defaults for interactive mode)
        nmap_ports = "22,23,80,443,502,5020,102,20000,2404,47808,4840" 
        nmap_flags = "-T4 -sS -A"
        nmap_vurnability_script = "default"
        print(f"{bcolors.BGTEXT}Debug: subnet={subnet}, range_start={range_start}, range_end={range_end}, option={answer}{bcolors.ENDC}")
        print(f"{bcolors.BGTEXT}Debug: ports={nmap_ports}, flags={nmap_flags}, vuln_script={nmap_vurnability_script}{bcolors.ENDC}")

    if not subnet or not range_start or not range_end:
        print(f"{bcolors.FAIL}Error: Subnet and range values must be provided.{bcolors.ENDC}")
        return

    os.makedirs("logs", exist_ok=True)

    if answer == "0":
        results = scan_active_hosts(subnet, range_start, range_end, nmap_flags, nmap_ports)
        if results:
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
                    print(f"Operating system: {details['os']}")
        else:
            print(f"{bcolors.WARNING}No hosts found or scan failed.{bcolors.ENDC}")

    elif answer == "1":
        scan_vurnabilities(subnet, range_start, range_end, nmap_flags, nmap_ports, nmap_vurnability_script)
    
    elif answer == "2":
        scan_modbus(subnet, range_start, range_end, nmap_flags)

    try:
        if os.path.exists("logs/hosts.xml"):
            with open("logs/hosts.xml") as xml_file, open("logs/hosts.json", "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
            print(f"{bcolors.OKGREEN}Converted hosts.xml to hosts.json{bcolors.ENDC}")
        if os.path.exists("logs/resources.xml"):
            with open("logs/resources.xml") as xml_file, open("logs/resources.json", "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
            print(f"{bcolors.OKGREEN}Converted resources.xml to resources.json{bcolors.ENDC}")
        if os.path.exists("logs/modbus.xml"):
            with open("logs/modbus.xml") as xml_file, open("logs/modbus.json", "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
            print(f"{bcolors.OKGREEN}Converted modbus.xml to modbus.json{bcolors.ENDC}")
        if os.path.exists("logs/vulnerabilities.xml"):
            with open("logs/vulnerabilities.xml") as xml_file, open("logs/vulnerabilities.json", "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
            print(f"{bcolors.OKGREEN}Converted vulnerabilities.xml to vulnerabilities.json{bcolors.ENDC}")
    except Exception as e:
        print(f"{bcolors.FAIL}Error while converting XML to JSON: {e}{bcolors.ENDC}")

    print(f"{bcolors.OKGREEN}Scan completed. Results saved in 'logs' directory.{bcolors.ENDC}")

if __name__ == "__main__":
    main()
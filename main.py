import subprocess, xmltodict, json, os

def scan_active_hosts(subnet, range_start, range_end):
    cmd = f"sudo nmap -sn {subnet}.{range_start}-{range_end} -oX logs/hosts.xml"
    subprocess.run(cmd, shell=True, capture_output=False, text=True)

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

    return hosts

def scan_open_ports(subnet, range_start, range_end):
    hosts = scan_active_hosts(subnet, range_start, range_end)
    for ip in hosts:
        cmd = f"sudo nmap {nmap_flags} -p {nmap_ports} -oX logs/resources.xml {ip}"
        print(cmd)
        subprocess.run(cmd, shell=True, capture_output=False, text=True)

        with open("logs/resources.xml", "r") as file:
            data = xmltodict.parse(file.read())

def scan_modbus(subnet, range_start, range_end):
    cmd = f"sudo nmap {nmap_flags} -p 22 {subnet}.{range_start}-{range_end} -oX logs/modbus.xml"
    subprocess.run(cmd, shell=True, capture_output=True, text=True)

def scan_vurnabilities(subnet, range_start, range_end):
    cmd_vuln = f"sudo nmap {nmap_flags} -p {nmap_ports} --script {nmap_vurnability_script} {subnet}.{range_start}-{range_end} -oX logs/vulnerabilities.xml"
    subprocess.run(cmd_vuln, shell=True, capture_output=True, text=True)

def convert_xml_to_json(xml_filename, json_filename):
    if os.path.exists(f"logs/{xml_filename}.xml"):
        try:
            with open(xml_filename) as xml_file, open(json_filename, "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        except Exception as e:
            return

def main():
    global nmap_ports, nmap_flags, nmap_vurnability_script
    nmap_ports = "22,23,80,443,502"
    nmap_flags = "-T4 -sS -A"
    nmap_vurnability_script = "default"

    subnet = "192.168.247"  
    range_start = "6"   
    range_end = "10"    
    answer = "1"        

    os.makedirs("logs", exist_ok=True)

    if answer == "0":
        scan_active_hosts(subnet, range_start, range_end)
    elif answer == "1":
        scan_open_ports(subnet, range_start, range_end)
    elif answer == "2":
        scan_vurnabilities(subnet, range_start, range_end)
    elif answer == "3":
        scan_modbus(subnet, range_start, range_end)

if __name__ == "__main__":
    main()
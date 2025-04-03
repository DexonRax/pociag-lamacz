from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, xmltodict, os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:5173"]}})
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Nmap Scanner API"})
def scan_active_hosts(subnet, range_start, range_end):
    cmd = f"sudo nmap -sn {subnet}.{range_start}-{range_end} -oX logs/hosts.xml"
    subprocess.run(cmd, shell=True, text=True)
    
    with open("logs/hosts.xml", "r") as file:
        data = xmltodict.parse(file.read())
    
    hosts = []
    if 'host' in data['nmaprun']:
        host_data = data['nmaprun']['host']
        if isinstance(host_data, list):
            for host in host_data:
                if isinstance(host['address'], list):
                    for addr in host['address']:
                        if addr['@addrtype'] == 'ipv4':
                            hosts.append(addr['@addr'])
                elif host['address']['@addrtype'] == 'ipv4':
                    hosts.append(host['address']['@addr'])
        elif isinstance(host_data, dict):
            if isinstance(host_data['address'], list):
                for addr in host_data['address']:
                    if addr['@addrtype'] == 'ipv4':
                        hosts.append(addr['@addr'])
            elif host_data['address']['@addrtype'] == 'ipv4':
                hosts.append(host_data['address']['@addr'])
    
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
    subprocess.run(cmd, shell=True, capture_output=False, text=True)

def scan_vurnabilities(subnet, range_start, range_end):
    cmd_vuln = f"sudo nmap {nmap_flags} -p {nmap_ports} --script {nmap_vurnability_script} {subnet}.{range_start}-{range_end} -oX logs/vulnerabilities.xml"
    subprocess.run(cmd_vuln, shell=True, capture_output=False, text=True)

#def convert_xml_to_json(xml_filename, json_filename):
    #if os.path.exists(f"logs/{xml_filename}.xml"):
        #try:
            #with open(xml_filename) as xml_file, open(json_filename, "w") as json_file:
                #json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        #except Exception as e:
            #return

@app.route('/scan-active-hosts', methods=['POST'])
def scan_hosts():
    data = request.get_json()
    subnet = data.get('subnet')
    range_start = data.get('range_start')
    range_end = data.get('range_end')
    
    if not all([subnet, range_start, range_end]):
        return jsonify({"error": "Missing parameters"}), 400
    
    os.makedirs("logs", exist_ok=True)
    hosts = scan_active_hosts(subnet, range_start, range_end)
    return jsonify({"hosts": hosts})

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

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    
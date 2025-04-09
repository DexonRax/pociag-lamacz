from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, xmltodict, os

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

def run_nmap_with_password(cmd, password):
    process = subprocess.Popen(
        ["sudo", "-S"] + cmd.split(), 
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    stdout, stderr = process.communicate(input=f"{password}\n")
    
    if "Sorry, try again" in stderr:
        raise Exception("Authentication failed: Incorrect password")
    
    return process.returncode

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
"""
#def convert_xml_to_json(xml_filename, json_filename):
    #if os.path.exists(f"logs/{xml_filename}.xml"):
        #try:
            #with open(xml_filename) as xml_file, open(json_filename, "w") as json_file:
                #json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        #except Exception as e:
            #return
"""

@app.route('/scan-active-hosts', methods=['POST'])
def scan_hosts():
    data = request.get_json()
    target = data.get('target')
    sudo_password = data.get('sudo_password')
    
    if not all([target, sudo_password]):
        return jsonify({"error": "Missing parameters"}), 400
    
    os.makedirs("logs", exist_ok=True)
    
    try:
        nmap_cmd = f"nmap -sn {target} -oX logs/hosts.xml"
        
        return_code = run_nmap_with_password(nmap_cmd, sudo_password)
        
        if return_code != 0:
            return jsonify({"error": f"Command failed with return code {return_code}"}), 500
        
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
            
        return jsonify({"hosts": hosts})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    
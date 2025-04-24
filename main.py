from flask import Flask, request, jsonify
from flask_cors import CORS
import subprocess, xmltodict, platform

OS = platform.system()
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": ["http://localhost:3000"]}})

def run_cmd_with_password(cmd, password):
    process = subprocess.Popen(
        ["sudo", "-S"] + cmd.split(),
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    stdout, stderr = process.communicate(input=f"{password}\n")

    if "Sorry, try again" in stderr:
        raise Exception("Uwierzytelnienie nieudane: złe hasło")

    return process.returncode, stdout

def use_cmd(data, cmd):
    sudo_password = data.get('sudo_password')

    if OS == "Windows":
        result = subprocess.run(cmd, shell=True, text=True, capture_output=True)
        output = result.stdout
        if result.returncode != 0:
            raise Exception(f"Błąd podczas wykonywania nmap: {result.stderr}")
    else:
        if not sudo_password:
            raise Exception("Wymagane hasło sudo")
        return_code, output = run_cmd_with_password(cmd, sudo_password)
        if return_code != 0:
            raise Exception(f"Komenda nieukończona z błędem: {return_code}")
            
    return xmltodict.parse(output)

def get_info(nmap_dict):
    raw_cmd = nmap_dict['nmaprun'].get('@args')
    info = []
    info.append({"cmd": raw_cmd})
    return info

def get_hosts(nmap_dict):
    raw_hosts = nmap_dict['nmaprun'].get('host', [])
    hosts = []

    if isinstance(raw_hosts, dict):
        raw_hosts = [raw_hosts]

    for host in raw_hosts:
        if isinstance(host, dict):
            addresses = host.get('address', [])
            hostnames = host.get('hostnames', {}).get('hostname', {})

            ip = None
            mac = None

            if isinstance(addresses, list):
                for addr in addresses:
                    if addr.get('@addrtype') == 'ipv4':
                        ip = addr.get('@addr')
                    elif addr.get('@addrtype') == 'mac':
                        mac = addr.get('@addr')
            elif isinstance(addresses, dict):
                if addresses.get('@addrtype') == 'ipv4':
                    ip = addresses.get('@addr')
                elif addresses.get('@addrtype') == 'mac':
                    mac = addresses.get('@addr')

            if isinstance(hostnames, list):
                hostname = hostnames[0].get('@name')
            elif isinstance(hostnames, dict):
                hostname = hostnames.get('@name')
            else:
                hostname = None

            if ip:
                hosts.append({
                    "ip": ip,
                    "mac": mac,
                    "name": hostname
                })

    return hosts

            
@app.route('/export', methods=['POST'])
def export():"""
    
    if os.path.exists(f"logs/{xml_filename}.xml"):
        try:
            with open(xml_filename) as xml_file, open(json_filename, "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        except Exception as e: 
            return jsonify({"błąd": str(e)}), 500
    """

@app.route('/scan-modbus-port', methods=['POST'])
def scan_modbus():
    data = request.get_json()
    target = data.get('target')
    flags = data.get('flags')

    if not all([target, flags]):
        return jsonify({"Błąd": "Brakujące elementy"}), 400

    try:
        nmap_cmd = f"nmap {flags} -p 22 {target}" # tu naprawic zeby mudbus byl xddd
        nmap_dict = use_cmd(data, nmap_cmd)

        data = get_hosts(nmap_dict) + get_info(nmap_dict)
        return jsonify({"data": data})
    
    except Exception as e:
        return jsonify({"błąd": str(e)}), 500

@app.route('/scan-active-hosts', methods=['POST'])
def scan_hosts():
    data = request.get_json()
    target = data.get('target')
    
    if not target:
        return jsonify({"Błąd": "Brakujące elementy"}), 400
    
    try:
        nmap_cmd = f"nmap -sn {target} -oX -"
        nmap_dict = use_cmd(data, nmap_cmd)

        data = get_hosts(nmap_dict) + get_info(nmap_dict)
        return jsonify({"data": data})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scan-ports', methods=['POST'])
def scan_ports():
    data = request.get_json()
    target = data.get('target')
    flags = data.get('flags')
    ports = data.get('ports')
    script = data.get('script')
    
    if not all([target, flags, ports, script]):
        return jsonify({"błąd": "Brakujące parametry"}), 400
    
    try:
        nmap_cmd = f"sudo nmap {flags} -p {ports} --script {script} {target}"
        nmap_dict = use_cmd(data, nmap_cmd)

        data = get_hosts(nmap_dict) + get_info(nmap_dict)
        return jsonify({"data": data})
    
    except Exception as e:
        return jsonify({"błąd": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    
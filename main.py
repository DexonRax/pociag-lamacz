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
    
    stderr = process.communicate(input=f"{password}\n")
    
    if "Sorry, try again" in stderr:
        raise Exception("Uwierzytelnienie nieudane: złe hasło")
    
    return process.returncode

@app.route('/scan-modbus-port', methods=['POST'])
def scan_modbus():
    data = request.get_json()
    target = data.get('target')
    flags = data.get('flags')
    sudo_password = data.get('sudo_password')

    if not all([target, sudo_password]):
        return jsonify({"Błąd": "Brakujące elementy"}), 400

    try:
        nmap_cmd = f"nmap {flags} -p 22 {target}" # tu naprawic zeby mudbus byl xddd
        
        return_code = run_nmap_with_password(nmap_cmd, sudo_password)
        
        if return_code != 0:
            return jsonify({"błąd": f"Komenda nieukończona z błędem: {return_code}"}), 500
        
        hosts = []
        
        return jsonify({"hosts": hosts})
    
    except Exception as e:
        return jsonify({"błąd": str(e)}), 500
    
@app.route('/export', methods=['POST'])
def export():
    if os.path.exists(f"logs/{xml_filename}.xml"):
        try:
            with open(xml_filename) as xml_file, open(json_filename, "w") as json_file:
                json.dump(xmltodict.parse(xml_file.read()), json_file, indent=4)
        except Exception as e: 
            return jsonify({"błąd": str(e)}), 500

@app.route('/scan-active-hosts', methods=['POST'])
def scan_hosts():
    data = request.get_json()
    target = data.get('target')
    sudo_password = data.get('sudo_password')
    
    if not all([target, sudo_password]):
        return jsonify({"Błąd": "Brakujące elementy"}), 400
    
    try:
        nmap_cmd = f"nmap -sn {target}"
        
        return_code = run_nmap_with_password(nmap_cmd, sudo_password)
        
        if return_code != 0:
            return jsonify({"błąd": f"Komenda nieukończona z błędem: {return_code}"}), 500
        
        hosts = []
        
        return jsonify({"hosts": hosts})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/scan-ports', methods=['POST'])
def scan_ports():
    data = request.get_json()
    target = data.get('target')
    flags = data.get('flags')
    ports = data.get('ports')
    script = data.get('script')
    sudo_password = data.get('sudo_password')
    
    if not all([target, sudo_password]):
        return jsonify({"błąd": "Brakujące parametry"}), 400
    
    try:
        nmap_cmd = f"sudo nmap {flags} -p {ports} --script {script} {target}"
        
        return_code = run_nmap_with_password(nmap_cmd, sudo_password)
        
        if return_code != 0:
            return jsonify({"błąd": f"Komenda nieukończona z błędem: {return_code}"}), 500
        
        hosts = []
    
            
        return jsonify({"hosts": hosts})
    
    except Exception as e:
        return jsonify({"błąd": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
    
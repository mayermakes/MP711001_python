#WORKING 4 channel!! no beeping anymore

from flask import Flask, request, jsonify, send_from_directory
import socket
import time

app = Flask(__name__, static_folder="static")

PSU_IP = "192.168.1.100"
PSU_PORT = 5025


class PSU:
    def __init__(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        self.sock.connect((PSU_IP, PSU_PORT))
        time.sleep(0.2)

    def write(self, cmd):
        self.sock.sendall((cmd + "\n").encode())
        time.sleep(0.1)

    def query(self, cmd):
        self.sock.sendall((cmd + "\n").encode())
        time.sleep(0.15)
        return self.sock.recv(1024).decode().strip()


psu = PSU()

active_channel = 1


@app.route("/")
def index():
    return send_from_directory("static", "index.html")


# -----------------------------
# SET (safe)
# -----------------------------
@app.route("/set", methods=["POST"])
def set_psu():
    global active_channel

    d = request.json
    ch = int(d["channel"])

    active_channel = ch

    psu.write(f"INST CH{ch}")
    time.sleep(0.2)

    if d.get("voltage") is not None:
        psu.write(f"VOLT {d['voltage']}")

    if d.get("current") is not None:
        psu.write(f"CURR {d['current']}")

    return jsonify({"ok": True})


# -----------------------------
# OUTPUT
# -----------------------------
@app.route("/output", methods=["POST"])
def output():
    d = request.json
    ch = int(d["channel"])

    psu.write(f"INST CH{ch}")
    time.sleep(0.2)

    psu.write(f"OUTP {'ON' if d['state'] else 'OFF'}")

    return jsonify({"ok": True})


# -----------------------------
# SINGLE CHANNEL MEASURE ONLY
# -----------------------------
@app.route("/measure")
def measure():
    global active_channel

    psu.write(f"INST CH{active_channel}")
    time.sleep(0.2)

    v = psu.query("MEAS:VOLT?")
    time.sleep(0.1)
    i = psu.query("MEAS:CURR?")

    return jsonify({
        "channel": active_channel,
        "voltage": v,
        "current": i
    })


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

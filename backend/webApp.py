from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, emit
from scapy.all import sniff, conf, IP
import threading

db = SQLAlchemy()
socketio = SocketIO()

app = Flask(__name__, template_folder='../frontend/templates', static_folder='../frontend/static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Scoreboard.db'

db.init_app(app)
socketio.init_app(app)

IP1 = "192.168.2.60"
IP2 = "192.168.2.42"

ETHERNET_INTERFACE = r"\Device\NPF_{65FB39AF-8813-4541-AC82-849B6D301CAF}"
# -------------------------------------------------| ROUTES |------------------------------------------------- #



@app.route('/')
def index():
    return render_template('index.html')



# -------------------------------------------------| SNIFFER |------------------------------------------------ #

def packet_callback(packet):
    if packet.haslayer(IP) and (packet[IP].src == IP1 or packet[IP].src == IP2):
        
        packet_info = packet.original.show(dump=True)
        packet_bytes = bytes(packet).hex()
        
        with open("packet.txt", "a") as f:
            f.write(str(packet_info))
            f.write("\n")
            f.write(str(packet_bytes))
            f.write("\n")
        
        
        socketio.emit('packet_data', {'data': packet_info + '\n' + packet_bytes})
    
    
    # if packet.haslayer(IP) and (packet[IP].dst == "192.168.1.126"):
    #     packet_info = packet.show(dump=True)
    #     packet_bytes = bytes(packet).hex()
    #     socketio.emit('packet_data', {'data': packet_info + '\n' + packet_bytes})
        
    
    #packet_info = packet.show(dump=True)
    #packet_bytes = bytes(packet).hex()
    
    #print(packet)
    #socketio.emit('packet_data', {'data': packet_info + '\n' + packet_bytes})
        

def start_sniffing():
    conf.L3socket = conf.L3socket
    print("Starting packet sniffer...")
    sniff(prn=packet_callback, store=False, iface=ETHERNET_INTERFACE)
    #sniff(prn=packet_callback, store=False)


# ---------------------------------------------| SOCKET HANDLING |------------------------------------------- #



@socketio.on('connect')
def handle_connect():
    print("Client connected")
    emit('server_response', {'message': 'Connected to the server!'})

@socketio.on('client_event')
def handle_client_event(json):
    print(f"Received event: {json}")
    emit('server_response', {'message': 'Received your event!'})
    
    
# ----------------------------------------------------------------------------------------------------------- #

sniffing_thread = threading.Thread(target=start_sniffing)
sniffing_thread.daemon = True 
sniffing_thread.start()
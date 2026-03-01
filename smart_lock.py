# smart_lock.py - Vulnerable IoT Device
import paho.mqtt.client as mqtt
import time
import json
import threading

# Using a public sandbox broker for the lab environment
MQTT_BROKER = "broker.emqx.io"
PORT = 1883
# Unique topic path for the lab
TOPIC_BASE = "enterprise/lab/smartlock/door_1"

# The secret PIN hardcoded or expected by the device
SECRET_PIN = "8472"

def on_connect(client, userdata, flags, rc, properties=None):
    print(f"[+] Smart Lock connected to IoT Broker. Listening for commands...")
    # The lock subscribes to its own command channel
    client.subscribe(f"{TOPIC_BASE}/command")

def on_message(client, userdata, msg):
    payload = msg.payload.decode()
    print(f"[*] Lock received command: {payload}")
    
    try:
        data = json.loads(payload)
        if data.get("action") == "UNLOCK" and data.get("pin") == SECRET_PIN:
            print("\n[!!!] VALID PIN RECEIVED. DOOR UNLOCKED. [!!!]\n")
        else:
            print("[-] Invalid command or PIN.")
    except:
        pass

def simulate_owner_traffic(client):
    """Simulates the homeowner unlocking the door periodically from their app."""
    while True:
        time.sleep(10)
        print("[*] Homeowner app sending unlock command...")
        payload = json.dumps({"action": "UNLOCK", "pin": SECRET_PIN})
        client.publish(f"{TOPIC_BASE}/command", payload)

if __name__ == "__main__":
    # THE FIX: Explicitly passing the Callback API Version for paho-mqtt 2.0+
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "SmartLock_Device")
    client.on_connect = on_connect
    client.on_message = on_message

    print("[*] Booting up IoT Smart Lock...")
    client.connect(MQTT_BROKER, PORT, 60)
    
    # Start the background thread simulating the owner
    threading.Thread(target=simulate_owner_traffic, args=(client,), daemon=True).start()
    
    client.loop_forever()
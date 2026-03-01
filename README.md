# IoT Insecure MQTT Protocol Exploitation

## 🎯 Executive Summary
This laboratory demonstrates the severe risks of insecure IoT communication protocols. Specifically, it targets an unauthenticated **MQTT (Message Queuing Telemetry Transport)** broker. The lab illustrates how an attacker can passively eavesdrop on a wildcard topic (`#`) to intercept sensitive plaintext telemetry (like a smart lock PIN), and then actively inject forged commands to hijack the hardware.

[Image of MQTT protocol architecture showing a publish-subscribe model with an unauthenticated broker being intercepted by an attacker]

---

## 🏗️ Technical Architecture

### 1. The Vulnerable IoT Device (`smart_lock.py`)
Simulates an enterprise smart door lock. It connects to an MQTT broker over plaintext port 1883 without requiring a client certificate or credentials. It expects a JSON payload containing a valid PIN to trigger the `UNLOCK` action.

### 2. The Attacker Engine (`mqtt_hijacker.py`)
An automated exploitation script that connects anonymously to the broker. 
* **Phase 1 (Eavesdropping):** Subscribes to the target's wildcard topic to sniff network traffic and extract the homeowner's secret PIN from the JSON payload.
* **Phase 2 (Command Injection):** Replays the intercepted PIN inside a forged `UNLOCK` payload, publishing it back to the broker to force the door open without the owner's consent.

---

## 🛡️ Remediation & Architectural Defense
IoT ecosystems must assume the network is hostile.

### The Professional Fix
1. **Transport Layer Security (MQTTS):** Never use plaintext port 1883. All MQTT traffic must be routed over port 8883 using TLS encryption to prevent packet sniffing.
2. **Broker Authentication:** The broker must strictly reject anonymous connections. Devices should authenticate using strong passwords or, ideally, mutual TLS (mTLS) with client certificates (X.509).
3. **Topic Access Control Lists (ACLs):** Devices and users should operate on a principle of least privilege. Clients should only have read/write access to their specific topics, and wildcard (`#`) subscriptions must be disabled for standard users.

---

## 🛠️ Laboratory Execution Steps

### 1. Clone the Repository
```bash
git clone [https://github.com/abhinandanpandey-in/IoT-MQTT-Lab.git](https://github.com/abhinandanpandey-in/IoT-MQTT-Lab.git)
cd IoT-MQTT-Lab
```
2. Initialize the Environment

```bash
python -m venv venv
# Windows
.\venv\Scripts\activate
# Linux/Mac
source venv/bin/activate

pip install paho-mqtt
```

3. Execute the Exploit
  1. Boot the IoT Device: Run python smart_lock.py to start the smart lock and simulate the homeowner.

  2. Launch the Hijacker: In a separate terminal, run python mqtt_hijacker.py.

  3. Observe the Breach: Watch the hijacker script intercept the owner's broadcasted PIN in plaintext, then instantly inject a forged payload to force the smart lock to open.

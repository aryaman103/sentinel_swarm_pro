import subprocess
import os
import logging

HONEYPOT_IMAGE = os.getenv("HONEYPOT_IMAGE", "honeypot-runner")
HONEYPOT_NETWORK = os.getenv("HONEYPOT_NETWORK", "default")

def spawn_honeypot(ip):
    # Spins up a new honeypot container with network alias
    container_name = f"honeypot_{ip.replace('.', '_')}"
    cmd = [
        "docker", "run", "-d",
        "--network", HONEYPOT_NETWORK,
        "--network-alias", ip,
        "--name", container_name,
        HONEYPOT_IMAGE
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, check=True, text=True)
        container_id = result.stdout.strip()
        logging.info(f"Honeypot spawned: {container_id} for {ip}")
        return container_id
    except Exception as e:
        logging.error(f"Failed to spawn honeypot: {e}")
        return None

def quarantine_ip(ip):
    # Appends to /etc/hosts.deny (assume root perms in container)
    try:
        with open("/etc/hosts.deny", "a") as f:
            f.write(f"ALL: {ip}
")
        logging.info(f"Quarantined IP: {ip}")
    except Exception as e:
        logging.error(f"Failed to quarantine IP: {e}")

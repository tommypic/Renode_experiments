import socket
import threading
import time
from Antmicro.Renode.Time import TimeInterval

# Configuration
UDP_IP = "0.0.0.0"
UDP_PORT = 12345

# Access the sensor once
sensor = self.Machine["sysbus.i2c1.dist_sensor"]

class LocalState:
    def __init__(self):
        self.last_distance = 10.0

state = LocalState()

def udp_worker():
    # Use a non-blocking socket approach or a short timeout
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        sock.bind((UDP_IP, UDP_PORT))
        # sock.setblocking(False) could be used, but settimeout is safer for this thread
        sock.settimeout(0.1)
        print("[UDP] Thread listening on port 12345")
    except Exception as err:
        print("[UDP] Bind failed: {}".format(err))
        return

    while True:
        try:
            data, addr = sock.recvfrom(1024)
            raw_str = data.decode("utf-8")
            state.last_distance = float(raw_str)
        except socket.timeout:
            # This prevents the thread from hanging indefinitely
            continue
        except Exception as err:
            # Log only once to avoid spamming the console
            pass

# Start the thread. Renode script execution continues while this runs in background.
t = threading.Thread(target=udp_worker)
t.daemon = True
t.start()

# Peripheral update hook (running in Renode virtual time)
def update_sensor_hook(*args):
    try:
        sensor.Distance = int(state.last_distance)
    except:
        pass
    finally:
        # Schedule next update
        self.Machine.ScheduleAction(TimeInterval.FromMilliseconds(50), update_sensor_hook)

# Start the virtual time loop
update_sensor_hook()
print("[HOOK] Unity bridge active. Renode is NOT blocked.")

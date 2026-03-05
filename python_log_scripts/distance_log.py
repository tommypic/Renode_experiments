# -*- coding: utf-8 -*-
import math
from Antmicro.Renode.Time import TimeInterval
import System.IO

pipe_path = "/home/tom/Renode_experiments/python_log_scripts/distance_status_pipe"

try:
    # Use os.open with O_NONBLOCK as it's the standard way for POSIX FIFOs logic
    # In IronPython, even if O_NONBLOCK isn't in 'os', we use O_NDELAY or rely on 
    # the fact that opening for writing a FIFO blocks until there's a reader.
    # To truly avoid blocking during 'open', we check if there's a reader first or
    # try to use a different approach.
    
    # Check if the pipe exists and has a reader (using a try/except with a timeout-like logic or non-blocking open)
    # Since IronPython's 'os' is limited, we'll use a safer .NET approach that checks for a reader
    # or just skips if it would block.
    
    import System.IO
    # We use a pattern that won't hang: only attempt open if we can do so safely or 
    # just catch the IO exception if it's not ready.
    pipe = None
    # On Linux, opening a FIFO for writing blocks until a reader is present.
    # To avoid this, we'd need O_NONBLOCK, which IronPython 'os' doesn't expose easily.
    # Alternative: Use a separate thread to open the pipe so Renode doesn't hang.
    
    def open_pipe_threaded():
        global pipe
        try:
            # This might still block the background thread, but won't hang Renode's main startup
            pipe_stream = System.IO.File.Open(pipe_path, System.IO.FileMode.Open, System.IO.FileAccess.Write, System.IO.FileShare.ReadWrite)
            pipe = System.IO.StreamWriter(pipe_stream)
            pipe.AutoFlush = True
            print("Distance pipe connected.")
        except:
            pass

    import threading
    t = threading.Thread(target=open_pipe_threaded)
    t.daemon = True
    t.start()
    
except Exception as e:
    print("Could not setup pipe thread: {}".format(e))
    pipe = None

sensor = self.Machine["sysbus.i2c1.dist_sensor"]

def log_distance(time):
    if pipe:
        try:
            seconds = float(time.TimeElapsed.TotalSeconds)
            current_dist = sensor.Distance
            pipe.WriteLine("[{:.2f}s] SENSOR DISTANCE: {}m".format(seconds, current_dist))
        except Exception as e:
            print("Logging error to distance pipe: {}".format(e))

# Fix: Added *args to handle the TimeInterval argument passed by Renode
def schedule_log(*args):
    log_distance(self.Machine.ElapsedVirtualTime)
    self.Machine.ScheduleAction(TimeInterval.FromMilliseconds(100), schedule_log)

schedule_log()

import math
from Antmicro.Renode.Time import TimeInterval

sensor = self.Machine["sysbus.i2c1.dist_sensor"]

def update_hook(time):
    seconds = float(time.TimeElapsed.TotalSeconds)
    distance = 1000 + 500 * math.sin(2 * math.pi * seconds / 5.0)
    sensor.Distance = int(distance)

# Fix: Added *args to handle the TimeInterval argument passed by Renode
def schedule_update(*args):
    update_hook(self.Machine.ElapsedVirtualTime)
    self.Machine.ScheduleAction(TimeInterval.FromMilliseconds(100), schedule_update)

schedule_update()

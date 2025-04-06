import traci
import sumolib
import matplotlib.pyplot as plt
from collections import defaultdict

# --- Edit these paths ---
sumo_binary = "sumo"  # or "sumo-gui"
net_file = "my_sumo_net.net.xml"
route_file = "routes.rou.xml"
# -------------------------

sumo_cmd = [sumo_binary, "-n", net_file, "-r", route_file]
traci.start(sumo_cmd)

# Store vehicle paths
vehicle_paths = defaultdict(list)

# Run simulation
step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for veh_id in traci.vehicle.getIDList():
        x, y = traci.vehicle.getPosition(veh_id)
        vehicle_paths[veh_id].append((x, y))
    step += 1

traci.close()

# Plotting
plt.figure(figsize=(12, 10))
for veh_id, path in vehicle_paths.items():
    xs, ys = zip(*path)
    plt.plot(xs, ys, label=veh_id)

plt.title("Vehicle Routes from SUMO Simulation")
plt.xlabel("X Coordinate")
plt.ylabel("Y Coordinate")
plt.legend(loc='upper right', fontsize='small', ncol=2)
plt.grid(True)
plt.savefig("vehicle_routes.png", dpi=300)
plt.show()

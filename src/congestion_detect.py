import traci
import sumolib

# Define a function to determine color based on speed
def get_color_by_speed(speed, max_speed):
    speed_ratio = speed / max_speed
    if speed_ratio > 0.75:
        return (0, 255, 0)  # Green for high speed
    elif speed_ratio > 0.5:
        return (255, 255, 0)  # Yellow for medium speed
    else:
        return (255, 0, 0)  # Red for low speed

# Start the SUMO simulation
sumoBinary = sumolib.checkBinary('sumo-gui')
traci.start([sumoBinary, "-c", "map/my_sumo_net.sumocfg"])

# Run the simulation
step = 0
while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    for veh_id in traci.vehicle.getIDList():
        speed = traci.vehicle.getSpeed(veh_id)
        max_speed = traci.vehicle.getAllowedSpeed(veh_id)
        color = get_color_by_speed(speed, max_speed)
        traci.vehicle.setColor(veh_id, color)
    step += 1

traci.close()

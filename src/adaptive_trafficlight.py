import traci
import sumolib

# ---- Traffic Light & Lane Setup ----
tls_id = "277248951"

# Lanes assumed based on connection info for 277248951:
# You should confirm these lane IDs using netedit or sumo-gui.
ns_lanes = ["431330678_0", "47442733_0"]  # North-South incoming lanes
ew_lanes = ["25439947#0_0", "25439947#0_1"]  # East-West incoming lanes

phase_ns = 0  # Phase 0 = GGGGrrrr (North-South green)
phase_ew = 2  # Phase 2 = rrrrGGGG (East-West green)

switch_interval = 15  # seconds between decisions

# ---- SUMO Simulation Setup ----
sumoBinary = sumolib.checkBinary("sumo-gui")  # Use "sumo" for non-GUI
traci.start([sumoBinary, "-c", "map/my_sumo_net.sumocfg"])

step = 0
last_switch = 0

def get_vehicle_count(lanes):
    return sum(traci.lane.getLastStepVehicleNumber(lane) for lane in lanes)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    step += 1

    if step - last_switch >= switch_interval:
        ns_count = get_vehicle_count(ns_lanes)
        ew_count = get_vehicle_count(ew_lanes)
        current_phase = traci.trafficlight.getPhase(tls_id)

        print(f"[{step}s] NS: {ns_count} | EW: {ew_count} | Phase: {current_phase}")

        if ns_count > ew_count:
            if current_phase != phase_ns:
                print("🔁 Switching to Phase 0 (North-South green)")
                traci.trafficlight.setPhase(tls_id, phase_ns)
        else:
            if current_phase != phase_ew:
                print("🔁 Switching to Phase 2 (East-West green)")
                traci.trafficlight.setPhase(tls_id, phase_ew)

        last_switch = step

traci.close()

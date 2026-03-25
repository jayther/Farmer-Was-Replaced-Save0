import common

num_flips = common.ceil(1000 / max_drones())
def flip():
	for _ in range(num_flips):
		do_a_flip()

drones = []
for _ in range(max_drones() - 1):
	drones.append(spawn_drone(flip))
	move(East)
flip()

common.wait_for_drones(drones)

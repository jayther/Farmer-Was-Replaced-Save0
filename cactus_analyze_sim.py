import cactus_brick_lb
import cactus_section

clear()
if sim_brick:
	runner = cactus_brick_lb.create_run(sim_goal, sim_presort)
else:
	runner = cactus_section.create_run(0, get_world_size() - 1, False, sim_presort)
runner()

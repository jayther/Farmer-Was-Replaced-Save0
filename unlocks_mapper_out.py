import common

unlocks = num_unlocked(upgrade_type)
resources = get_cost(upgrade_type)

if resources == {}:
	common.wait(0.2)
else:
	quick_print('\t\t', resources, ',')
import common


unlocks = {}
items = {}
globals = {}
seed = 1
filename = 'fastest_lb'
speedup = 32

def print_readable(seconds):
	hours = common.floor(seconds / (60 * 60))
	rem_seconds = seconds - hours * 60 * 60
	minutes = common.floor(rem_seconds / 60)
	rem_seconds -= minutes * 60
	quick_print(hours, ':', minutes, ':', rem_seconds)


#duration = simulate(filename, unlocks, items, globals, seed, speedup)
duration = leaderboard_run(Leaderboards.Fastest_Reset, filename, 1000)

if duration != None:
	quick_print('Finished in', duration, 's')
	print_readable(duration)

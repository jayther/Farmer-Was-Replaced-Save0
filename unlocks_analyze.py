import common

unlock_map = {
	Unlocks.Grass : [
		{} ,
		{Items.Hay:300} ,
		{Items.Wood:500} ,
		{Items.Wood:2500} ,
		{Items.Wood:12500} ,
		{Items.Wood:62500} ,
		{Items.Wood:312000} ,
		{Items.Wood:1560000} ,
		{Items.Wood:7810000} ,
		{Items.Wood:39100000}
	],
	Unlocks.Speed : [
		{Items.Hay:20} ,
		{Items.Wood:20} ,
		{Items.Wood:50,Items.Carrot:50} ,
		{Items.Carrot:500} ,
		{Items.Carrot:1000}
	],
	Unlocks.Expand : [
		{Items.Hay:30} ,
		{Items.Wood:20} ,
		{Items.Wood:30,Items.Carrot:20} ,
		{Items.Wood:100,Items.Carrot:50} ,
		{Items.Pumpkin:1000} ,
		{Items.Pumpkin:8000} ,
		{Items.Pumpkin:64000} ,
		{Items.Pumpkin:512000} ,
		{Items.Pumpkin:4100000}
	],
	Unlocks.Plant : [
		{Items.Hay:50}
	],
	Unlocks.Carrots : [
		{Items.Wood:50} ,
		{Items.Wood:250} ,
		{Items.Wood:1250} ,
		{Items.Wood:6250} ,
		{Items.Wood:31200} ,
		{Items.Wood:156000} ,
		{Items.Wood:781000} ,
		{Items.Wood:3910000} ,
		{Items.Wood:19500000} ,
		{Items.Wood:97700000}
	],
	Unlocks.Pumpkins : [
		{Items.Wood:500,Items.Carrot:200} ,
		{Items.Carrot:1000} ,
		{Items.Carrot:4000} ,
		{Items.Carrot:16000} ,
		{Items.Carrot:64000} ,
		{Items.Carrot:256000} ,
		{Items.Carrot:1020000} ,
		{Items.Carrot:4100000} ,
		{Items.Carrot:16400000} ,
		{Items.Carrot:65500000}
	],
	Unlocks.Cactus : [
		{Items.Pumpkin:5000} ,
		{Items.Pumpkin:20000} ,
		{Items.Pumpkin:120000} ,
		{Items.Pumpkin:720000} ,
		{Items.Pumpkin:4320000} ,
		{Items.Pumpkin:25900000}
	],
	Unlocks.Dinosaurs : [
		{Items.Cactus:2000} ,
		{Items.Cactus:12000} ,
		{Items.Cactus:72000} ,
		{Items.Cactus:432000} ,
		{Items.Cactus:2590000} ,
		{Items.Cactus:15600000}
	],
	Unlocks.Fertilizer : [
		{Items.Wood:500} ,
		{Items.Wood:1500} ,
		{Items.Wood:9000} ,
		{Items.Wood:54000}
	],
	Unlocks.Mazes : [
		{Items.Weird_Substance:1000} ,
		{Items.Cactus:12000} ,
		{Items.Cactus:72000} ,
		{Items.Cactus:432000} ,
		{Items.Cactus:2590000} ,
		{Items.Cactus:15600000}
	],
	Unlocks.Megafarm : [
		{Items.Gold:2000} ,
		{Items.Gold:8000} ,
		{Items.Gold:32000} ,
		{Items.Gold:128000} ,
		{Items.Gold:512000}
	],
	Unlocks.Watering : [
		{Items.Wood:50} ,
		{Items.Wood:200} ,
		{Items.Wood:800} ,
		{Items.Wood:3200} ,
		{Items.Wood:12800} ,
		{Items.Wood:51200} ,
		{Items.Wood:205000} ,
		{Items.Wood:819000} ,
		{Items.Wood:3280000}
	],
	Unlocks.Sunflowers : [
		{Items.Carrot:500}
	],
	Unlocks.Trees : [
		{Items.Wood:50,Items.Carrot:70} ,
		{Items.Hay:300} ,
		{Items.Hay:1200} ,
		{Items.Hay:4800} ,
		{Items.Hay:19200} ,
		{Items.Hay:76800} ,
		{Items.Hay:307000} ,
		{Items.Hay:1230000} ,
		{Items.Hay:4920000} ,
		{Items.Hay:19700000}
	],
	Unlocks.Leaderboard : [
		{Items.Bone:2000000,Items.Gold:1000000}
	]
}

def calc_sum_cost(cost):
	sum = 0
	for item_type in cost:
		sum += cost[item_type]
	return sum

unlocked_all = False
step = 0
while not unlocked_all:
	lowest_type = Unlocks.Grass
	lowest_sum = -1
	lowest_cost = {}
	
	unlocked_all = True
	for type in unlock_map:
		if len(unlock_map[type]) == 0:
			continue
		unlocked_all = False
		cost = unlock_map[type][0]
		sum = calc_sum_cost(cost)
		if lowest_sum == -1 or sum < lowest_sum:
			lowest_type = type
			lowest_sum = sum
			lowest_cost = cost
	
	if not unlocked_all:
		unlock_map[lowest_type].pop(0)
		quick_print('(', lowest_type, ',', lowest_cost, '),')
		step += 1
	

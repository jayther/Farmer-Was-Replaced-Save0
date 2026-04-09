
step_map = [
	( Unlocks.Speed , {Items.Hay:20} ),
	( Unlocks.Expand , {Items.Hay:30} ), # 1x3
	( Unlocks.Plant , {Items.Hay:50} ), # first plant (bush)
	( Unlocks.Speed , {Items.Wood:20} ),
	( Unlocks.Expand , {Items.Wood:20} ), # 3x3
	( Unlocks.Carrots , {Items.Wood:50} ), # first carrots
	( Unlocks.Expand , {Items.Wood:30,Items.Carrot:20} ), # 4x4
	( Unlocks.Speed , {Items.Wood:50,Items.Carrot:50} ),
	( Unlocks.Trees , {Items.Wood:50,Items.Carrot:70} ), # first trees
	( Unlocks.Sunflowers , {Items.Carrot:500} ), # first (and only) sunflowers
	( Unlocks.Expand , {Items.Wood:100,Items.Carrot:50} ), # 6x6
	( Unlocks.Grass , {Items.Hay:300} ),
	( Unlocks.Watering , {Items.Wood:50} ), # first watering
	( Unlocks.Watering , {Items.Wood:200} ),
	( Unlocks.Carrots , {Items.Wood:250} ),
	( Unlocks.Grass , {Items.Wood:500} ),
	( Unlocks.Fertilizer , {Items.Wood:500} ), # first fertilizer
	( Unlocks.Fertilizer , {Items.Wood:1500} ),
	( Unlocks.Fertilizer , {Items.Wood:9000} ),
	( Unlocks.Trees , {Items.Hay:300} ),
	( Unlocks.Speed , {Items.Carrot:500} ),
	( Unlocks.Watering , {Items.Wood:800} ),
	( Unlocks.Speed , {Items.Carrot:1000} ),
	( Unlocks.Pumpkins , {Items.Wood:500,Items.Carrot:200} ), # first pumpkins
	( Unlocks.Pumpkins , {Items.Carrot:1000} ),
	( Unlocks.Expand , {Items.Pumpkin:1000} ), # 8x8
	( Unlocks.Trees , {Items.Hay:1200} ),
	( Unlocks.Carrots , {Items.Wood:1250} ),
	( Unlocks.Grass , {Items.Wood:2500} ),
	( Unlocks.Watering , {Items.Wood:3200} ),
	( Unlocks.Pumpkins , {Items.Carrot:4000} ),
	( Unlocks.Trees , {Items.Hay:4800} ),
	( Unlocks.Carrots , {Items.Wood:6250} ),
	( Unlocks.Expand , {Items.Pumpkin:8000} ), # 12x12
	( Unlocks.Grass , {Items.Wood:12500} ),
	( Unlocks.Watering , {Items.Wood:12800} ),
	( Unlocks.Pumpkins , {Items.Carrot:16000} ),
	( Unlocks.Trees , {Items.Hay:19200} ),
	( Unlocks.Carrots , {Items.Wood:31200} ),
	( Unlocks.Cactus , {Items.Pumpkin:5000} ), # first cactus
	( Unlocks.Cactus , {Items.Pumpkin:20000} ),
	( Unlocks.Mazes , {Items.Weird_Substance:1000} ), # first mazes
	( Unlocks.Mazes , {Items.Cactus:12000} ),
	( Unlocks.Mazes , {Items.Cactus:72000} ),
	( Unlocks.Megafarm , {Items.Gold:2000} ), # first megafarm (2 drones)
	( Unlocks.Megafarm , {Items.Gold:8000} ), # 4 drones
	( Unlocks.Megafarm , {Items.Gold:32000} ), # 8 drones
	( Unlocks.Polyculture , {Items.Pumpkin:3000} ), # first polyculture
	( Unlocks.Dinosaurs , {Items.Cactus:2000} ), # first dinosaur
	( Unlocks.Dinosaurs , {Items.Cactus:12000} ),
	( Unlocks.Dinosaurs , {Items.Cactus:72000} ),
	( Unlocks.Polyculture , {Items.Bone:10000} ),
	( Unlocks.Polyculture , {Items.Bone:50000} ),
	( Unlocks.Watering , {Items.Wood:51200} ),
	( Unlocks.Fertilizer , {Items.Wood:54000} ),
	( Unlocks.Grass , {Items.Wood:62500} ),
	( Unlocks.Megafarm , {Items.Gold:128000} ), # 16 drones
	( Unlocks.Expand , {Items.Pumpkin:64000} ), # 16x16
	( Unlocks.Pumpkins , {Items.Carrot:64000} ),
	( Unlocks.Trees , {Items.Hay:76800} ),
	( Unlocks.Cactus , {Items.Pumpkin:120000} ),
	( Unlocks.Carrots , {Items.Wood:156000} ),
	( Unlocks.Watering , {Items.Wood:205000} ),
	( Unlocks.Pumpkins , {Items.Carrot:256000} ),
	( Unlocks.Trees , {Items.Hay:307000} ),
	( Unlocks.Grass , {Items.Wood:312000} ),
	( Unlocks.Polyculture , {Items.Bone:250000} ),
	( Unlocks.Dinosaurs , {Items.Cactus:432000} ),
	( Unlocks.Mazes , {Items.Cactus:432000} ),
	( Unlocks.Expand , {Items.Pumpkin:512000} ), # 22x22
	( Unlocks.Megafarm , {Items.Gold:512000} ), # 32 drones
	( Unlocks.Cactus , {Items.Pumpkin:720000} ),
	( Unlocks.Carrots , {Items.Wood:781000} ),
	#( Unlocks.Watering , {Items.Wood:819000} ),
	( Unlocks.Pumpkins , {Items.Carrot:1020000} ),
	( Unlocks.Trees , {Items.Hay:1230000} ),
	( Unlocks.Polyculture , {Items.Bone:1250000} ),
	( Unlocks.Grass , {Items.Wood:1560000} ),
	( Unlocks.Dinosaurs , {Items.Cactus:2590000} ),
	( Unlocks.Mazes , {Items.Cactus:2590000} ),
	( Unlocks.Leaderboard , {Items.Bone:2000000,Items.Gold:1000000} ),
	#( Unlocks.Watering , {Items.Wood:3280000} ),
	( Unlocks.Carrots , {Items.Wood:3910000} ),
	( Unlocks.Expand , {Items.Pumpkin:4100000} ), # 32x32
	( Unlocks.Pumpkins , {Items.Carrot:4100000} ),
	( Unlocks.Cactus , {Items.Pumpkin:4320000} ),
	( Unlocks.Trees , {Items.Hay:4920000} ),
	( Unlocks.Grass , {Items.Wood:7810000} ),
	( Unlocks.Dinosaurs , {Items.Cactus:15600000} ),
	( Unlocks.Mazes , {Items.Cactus:15600000} ),
	( Unlocks.Pumpkins , {Items.Carrot:16400000} ),
	( Unlocks.Carrots , {Items.Wood:19500000} ),
	( Unlocks.Trees , {Items.Hay:19700000} ),
	( Unlocks.Cactus , {Items.Pumpkin:25900000} ),
	( Unlocks.Grass , {Items.Wood:39100000} ),
	( Unlocks.Pumpkins , {Items.Carrot:65500000} ),
	( Unlocks.Carrots , {Items.Wood:97700000} )
]



entity_unlock_map = {
	Entities.Grass: Unlocks.Grass,
	Entities.Bush: Unlocks.Trees,
	Entities.Tree: Unlocks.Trees,
	Entities.Carrot: Unlocks.Carrots,
	Entities.Pumpkin: Unlocks.Pumpkins,
	Entities.Cactus: Unlocks.Cactus,
	Entities.Treasure: Unlocks.Mazes,
	Entities.Sunflower: Unlocks.Sunflowers
}

item_unlock_map = {
	Items.Hay: Unlocks.Grass,
	Items.Wood: Unlocks.Trees,
	Items.Carrot: Unlocks.Carrots,
	Items.Pumpkin: Unlocks.Pumpkins,
	Items.Cactus: Unlocks.Cactus,
	Items.Bone: Unlocks.Dinosaurs,
	Items.Weird_Substance: Entities.Hedge,
	Items.Gold: Entities.Treasure,
	Items.Power: None
}

entity_item_map = {
	Entities.Apple: None,
	Entities.Bush: Items.Wood,
	Entities.Cactus: Items.Cactus,
	Entities.Carrot: Items.Carrot,
	Entities.Dead_Pumpkin: None,
	Entities.Dinosaur: None,
	Entities.Grass: Items.Hay,
	Entities.Hedge: None,
	Entities.Pumpkin: Items.Pumpkin,
	Entities.Sunflower: Items.Power,
	Entities.Treasure: Items.Gold,
	Entities.Tree: Items.Wood
}

def get_item_from_entity(entity_type):
	if entity_type not in entity_item_map:
		return None
	return entity_item_map[entity_type]

def get_unlock_type_from_entity(entity_type):
	if entity_type not in entity_unlock_map:
		return None
	return entity_unlock_map[entity_type]

def get_unlock_type_from_item(item_type):
	if item_type not in item_unlock_map:
		return None
	return item_unlock_map[item_type]
	
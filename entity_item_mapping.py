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

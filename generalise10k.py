from result import Results

class Generalise10k:
    def __init__(self, context, buildings, groups_dict):
        self.context = context
        self.buildings = buildings
        self.groups_dict = groups_dict

    def run(self):
        eliminated_buildings = []
        rectangelized_buildings = []
        for_manual_revision_buildings = []

        for building in self.buildings:
            if building.area < 40 and building.groupId is None:
                eliminated_buildings.append(building)
            elif building.isRectangle:
                rectangelized_buildings.append(building)
            else:
                for_manual_revision_buildings.append(building)

        return Results(
            eliminated_buildings = eliminated_buildings,
            rectangelized_buildings = rectangelized_buildings,
            for_manual_revision_buildings = for_manual_revision_buildings
        )

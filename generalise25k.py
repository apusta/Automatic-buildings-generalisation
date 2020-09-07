from context import Mode
from result import Results


class Generalise25k:
    def __init__(self, context, buildings, groups_dict):
        self.context = context
        self.buildings = buildings
        self.groups_dict = groups_dict

    def run(self):
        eliminated_buildings = []
        rectangelized_buildings = []
        for_manual_revision_buildings = []
        signatured_buildings = []
        unioned_groups = []
        typificated_groups = []

        # handle non grouped buildings
        for building in self.buildings:
            if building.groupId is None:
                if building.area <= 40:
                    eliminated_buildings.append(building)
                elif 100 > building.area > 40:
                    building.sygnature_rotation_count()
                    signatured_buildings.append(building)
                elif building.isRectangle:
                    rectangelized_buildings.append(building)
                else:
                    for_manual_revision_buildings.append(building)
            elif building.groupId and building.groupId not in self.groups_dict:
                if building.isRectangle:
                    rectangelized_buildings.append(building)
                else:
                    for_manual_revision_buildings.append(building)


        # handle grouped buildings
        for group in self.groups_dict.values():
            if self.context.mode == Mode.UNION:
                group.union()
                unioned_groups.append(group)
            elif self.context.mode == Mode.TYPIFICATION:
                group.typification()
                typificated_groups.append(group)

        return Results(
            eliminated_buildings=eliminated_buildings,
            rectangelized_buildings=rectangelized_buildings,
            for_manual_revision_buildings=for_manual_revision_buildings,
            signatured_buildings=signatured_buildings,
            unioned_groups=unioned_groups,
            typificated_groups=typificated_groups
        )

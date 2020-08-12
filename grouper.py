from group import Group
import uuid


class Grouper:
    @staticmethod
    def run(buildings):
        groups_dict = {}
        for building in buildings:
            print(building.properties["OBJECTID"])
            connected_with = []
            for building2 in buildings:
                if building2 == building:
                    continue

                if building.isConnected(building2):
                    connected_with.append(building2)

            if len(connected_with) > 0:
                group_ids = []
                for b in connected_with:
                    if b.groupId is not None:
                        group_ids.append(b.groupId)

                if len(group_ids) == 1:
                    group_buildings = [building] + connected_with + groups_dict[group_ids[0]].buildings
                    group_buildings = list(set(group_buildings))

                    groups_dict[group_ids[0]].buildings = group_buildings

                    for b in group_buildings:
                        b.groupId = group_ids[0]
                else:
                    groups = [groups_dict.get(id) for id in group_ids]

                    merged_group_buildings = [building] + connected_with + Grouper.__unpack_buildings_from_groups(groups)
                    merged_group_buildings = list(set(merged_group_buildings))

                    new_group = Group(uuid.uuid4(), merged_group_buildings)
                    groups_dict[new_group.id] = new_group

                    for group_id in group_ids:
                        groups_dict.pop(group_id, None)

                    for b in new_group.buildings:
                        b.groupId = new_group.id
        return groups_dict

    @staticmethod
    def __unpack_buildings_from_groups(groups):
        unpacked_buildings = []
        for g in groups:
            unpacked_buildings = unpacked_buildings + g.buildings

        return unpacked_buildings

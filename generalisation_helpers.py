class GeneralisationHelpers:
    @staticmethod
    def validate_groups(groups_dict):
        not_valid_groups = {}
        for key in list(groups_dict):
            g = groups_dict[key]
            g.set_type()
            if g.type == g.error_group_type:
                groups_dict.pop(g.id)
                not_valid_groups[g.id] = g

        return groups_dict, not_valid_groups

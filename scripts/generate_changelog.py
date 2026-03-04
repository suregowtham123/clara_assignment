def generate_changelog(v1_data, v2_data):

    changes = []

    for key in v1_data:

        if v1_data[key] != v2_data.get(key):

            old_value = v1_data[key]
            new_value = v2_data.get(key)

            change = f"{key} changed from {old_value} to {new_value}"
            changes.append(change)

    return changes
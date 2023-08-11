import samples

#


def mapping_fn(input_data, mapping_schema):
    output_data = {}

    for output_path, input_field in mapping_schema.items():
        input_action = input_field.pop("action")
        output_path_data = output_path.split("/")
        if input_action == "as_is":
            input_path_data = tuple(input_field["path"].split("/"))
            required_value = get_nested_value(input_data, input_path_data)
        elif input_action == "condition":
            condition_data = input_field[input_action].split(" ")
            is_condition_true = samples.actions[condition_data[1]](
                condition_data[0], condition_data[2]
            )
            if is_condition_true:
                # check if has #
                required_value = input_field["true"]
            else:
                required_value = input_field["false"]

        else:
            for key, value in input_field.items():
                if "#" in value:
                    input_path_data = value.strip("#").split("/")

                    input_field[key] = get_nested_value(input_data, input_path_data)

            required_value = samples.actions[input_action](**input_field)

        output_branch = build_output_branch(required_value, output_path_data)
        output_data = implement_output_branch(output_data, output_branch)
    print(output_data)


# input data = dictionary from xml, path data (tuple, with, values)
def get_nested_value(input_data, path_data):
    if type(input_data) == dict:
        return get_nested_value(input_data[path_data[0]], path_data[1:])
    else:
        return input_data


# Creates a dictionary that represents one path of the output_data dictionary
def build_output_branch(
    required_value,
    output_path_data,
):
    if len(output_path_data) == 0:
        return required_value
    else:
        return {
            output_path_data[0]: build_output_branch(
                required_value, output_path_data[1:]
            )
        }


def implement_output_branch(output_data, new_branch):
    new_output_data = output_data

    if len(output_data) == 0:
        new_output_data.update(new_branch)
        return new_output_data

    for key, value in new_branch.items():
        if key in new_output_data:
            new_output_data.update(
                {key: implement_output_branch(new_output_data[key], value)}
            )
            return new_output_data
        else:
            new_output_data.update(new_branch)

            return new_output_data


def process_condition(input_field, input_action):
    condition_data = input_field[input_action].split(" ")

    is_condition_true = samples.actions[condition_data[1]](
        condition_data[0], condition_data[2]
    )
    if is_condition_true:
        # check if has #
        required_value = input_field["true"]
    else:
        required_value = input_field["false"]


mapping_fn(samples.sample_dict, samples.sample_schema)

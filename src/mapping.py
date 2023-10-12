import actions


def mapping_fn(input_data, mapping_schema):
    output_data = {}

    for output_path, input_field in mapping_schema.items():
        input_action = input_field.pop("action")
        output_path_data = output_path.split("/")

        # passes the data exactly as it is without transformation
        if input_action == "as_is":
            input_path_data = tuple(input_field["path"].split("/"))
            required_value = get_nested_value(input_data, input_path_data)
        # passes data based on condition, allows for reference values
        elif input_action == "condition":
            required_value = process_condition(input_field, input_action, input_data)
        elif input_action == "text_formatting":
            required_value = process_text_formatting(input_field,input_action,input_data)
        elif input_action == "calc":
            required_value = process_calculation(input_data, input_field["expression"])
        else:
            for key, value in input_field.items():
                if "#" in value:
                    input_path_data = value.strip("#").split("/")

                    input_field[key] = get_nested_value(input_data, input_path_data)

            required_value = actions.actions[input_action](**input_field)

        output_branch = build_output_branch(required_value, output_path_data)
        output_data = implement_output_branch(output_data, output_branch)
    print(output_data)
    return output_data


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

# introduces the branch created in build_output_branch into the json without breaking already existing values and nested dict
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


def process_condition(input_field, input_action, input_data):
    condition_data = input_field[input_action].split(" ")
    # These two if statements check if either side of the equation is a reference to another value in the json and replaces the path with that data
    if condition_data[0][0] == "#":
        condition_data[0] = get_nested_value(input_data, condition_data[0].strip("#").split("/"))
    if condition_data[2][0] == "#":
        condition_data[2] = get_nested_value(input_data, condition_data[2].strip("#").split("/"))
    is_condition_true = actions.actions[condition_data[1]](
        condition_data[0], condition_data[2]
    )
    if is_condition_true:
        # check if the true value is a path to another value in the json
        if isinstance(input_field["true"], dict):
            required_value = perform_nested_action(input_data, input_field["true"])
        elif input_field["true"][0] == "#":
            required_value = get_nested_value(input_data, input_field["true"].strip("#").split("/"))
        else:
            required_value = input_field["true"]
    else:
        # check if the false value is a path to another value in the json
        if isinstance(input_field["false"], dict):
            required_value = perform_nested_action(input_data, input_field["true"])
        elif input_field["false"][0] == "#":
            required_value = get_nested_value(input_data, input_field["false"].strip("#").split("/"))
        else:
            required_value = input_field["false"]
    return required_value

def process_text_formatting(input_field, input_action,input_data):
    value_to_format = get_nested_value(input_data, input_field["path"].split("/"))
    # parameters = input_field["parameters"].split(" ")
    parameters = dict(parameter.split("=") for parameter in input_field["parameters"].split(" "))    
    arguments = {"action":input_field["format_type"], "text": value_to_format, **parameters}
    return actions.actions[input_action](**arguments)

def process_calculation(input_data, calculation_field):
    print("FIELD:")
    print(calculation_field)
    op_bracket_indexes = []
    cl_bracket_indexes = [] 
    for index, element in enumerate(calculation_field):
        if element == "(":
            op_bracket_indexes.append(index)
        elif element == ")":
            cl_bracket_indexes.append(index)

    
    print("RESULTS:")
    print(op_bracket_indexes)
    print(cl_bracket_indexes)


def perform_nested_action(input_data, action_field):
    
    input_action = action_field.pop("action")
    # passes the data exactly as it is without transformation
    if input_action == "as_is":
        input_path_data = tuple(action_field["path"].split("/"))
        required_value = get_nested_value(input_data, input_path_data)
    # passes data based on condition, allows for reference values
    elif input_action == "condition":
        required_value = process_condition(action_field, input_action, input_data)
    elif input_action == "text_formatting":
        required_value = process_text_formatting(action_field,input_action,input_data)
    elif input_action == "calc":
        required_value = process_calculation(input_data, action_field["expression"])

    else:
        for key, value in action_field.items():
            if "#" in value:
                input_path_data = value.strip("#").split("/")
                action_field[key] = get_nested_value(input_data, input_path_data)
        required_value = actions.actions[input_action](**action_field)

    return required_value
mapping_fn(actions.sample_dict, actions.sample_schema)
import pytest
import src.mapping as mapping
import tests.test_data.samples as samples


def test_get_nested_value_success():
    mock_input_data = samples.sample_dict
    mock_path_data = ["namespace:Invoice", "namespace:Node1", "@Code"]
    expected_result = 7
    actual_result = mapping.get_nested_value(mock_input_data, mock_path_data)
    assert expected_result == actual_result


def test_get_nested_value_failure():
    mock_input_data = samples.sample_dict
    erronous_path_data = "wrong"
    with pytest.raises(Exception) as excinfo:
        mapping.get_nested_value(mock_input_data, erronous_path_data)
    assert (
        "The path data passed in is not of the correct type. Type of the path: <class 'str'>. Path: wrong"
        in str(excinfo.value)
    )


def test_build_output_branch_success():
    mock_required_value = 12
    output_path_data = ["something", "here"]
    expected_result = {"something": {"here": 12}}
    actual_result = mapping.build_output_branch(
        mock_required_value, output_path_data
    )
    assert type(actual_result) is dict
    assert expected_result == actual_result


def test_build_output_branch_failure():
    mock_required_value = 12
    erronous_output_path_data = 500
    with pytest.raises(Exception):
        mapping.build_output_branch(
            mock_required_value, erronous_output_path_data
        )


def test_implement_output_branch_success():
    mock_output_data_1 = {"mock_value_1": 1, "mock_value_2": "example"}
    mock_new_branch_1 = {"branch_node": {"final_value": 12}}
    mock_output_data_2 = {
        "mock_value_1": 1,
        "branch_node": {"existing_value": "example_str"},
    }
    mock_new_branch_2 = {"branch_node": {"final_value": "string_value"}}

    expected_result_1 = {
        "mock_value_1": 1,
        "mock_value_2": "example",
        "branch_node": {"final_value": 12},
    }
    expected_result_2 = {
        "mock_value_1": 1,
        "branch_node": {
            "existing_value": "example_str",
            "final_value": "string_value",
        },
    }

    actual_result_1 = mapping.implement_output_branch(
        mock_output_data_1, mock_new_branch_1
    )
    actual_result_2 = mapping.implement_output_branch(
        mock_output_data_2, mock_new_branch_2
    )

    assert type(actual_result_1) is dict
    assert type(actual_result_2) is dict
    assert expected_result_1 == actual_result_1
    assert expected_result_2 == actual_result_2


def test_implement_output_branch_failure():
    erronous_new_branch = 15
    erronous_output_data = {
        "mock_value_1": 1,
        "branch_node": {"existing_value": "example_str"},
    }
    with pytest.raises(Exception):
        mapping.implement_output_branch(
            erronous_output_data, erronous_new_branch
        )


def test_process_condition_success():
    mock_input_field = {
        "condition": "#namespace:Invoice/namespace:Node1/@Code < 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    }
    mock_input_action = "condition"
    mock_input_data_1 = {
        "namespace:Invoice": {
            "namespace:Node1": {"@Code": 2, "@Title": "some_title"}
        }
    }
    mock_input_data_2 = {
        "namespace:Invoice": {
            "namespace:Node1": {"@Code": 7, "@Title": "some_title"}
        }
    }
    expected_result_1 = "some_title"
    expected_result_2 = 7
    actual_result_1 = mapping.process_condition(
        mock_input_field, mock_input_action, mock_input_data_1
    )
    actual_result_2 = mapping.process_condition(
        mock_input_field, mock_input_action, mock_input_data_2
    )
    assert expected_result_1 == actual_result_1
    assert expected_result_2 == actual_result_2


def test_process_condition_failure():
    erronous_input_field_1 = {
        "error": "#namespace:Invoice/namespace:Node1/@Code < 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    }
    erronous_input_field_2 = {
        "condition": "namespace:Invoice/namespace:Node1/@Code < 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    }
    mock_input_action = "condition"
    mock_input_data = {}
    with pytest.raises(Exception):
        mapping.process_condition(
            erronous_input_field_1, mock_input_action, mock_input_data
        )
    with pytest.raises(Exception):
        mapping.process_condition(
            erronous_input_field_2, mock_input_action, mock_input_data
        )


def test_process_text_formatting_success():
    mock_input_field = {
        "format_type": "encode",
        "parameters": "encoding=ascii errors=strict",
        "path": "namespace:Invoice/namespace:Node1/@Title",
    }

    mock_input_action = "text_formatting"
    mock_input_data = {
        "namespace:Invoice": {
            "namespace:Node1": {
                "@Code": 7,
                "@Title": "ExampleTitle",
            },
        }
    }
    expected_result = b"ExampleTitle"
    actual_result = mapping.process_text_formatting(
        mock_input_field, mock_input_action, mock_input_data
    )

    assert expected_result == actual_result


def test_process_text_formatting_failure():
    erronous_input_field = {
        "format_type": "encode",
        "parameters": "encoding=ascii errors=strict",
        "path": "namespace:Invoice/namespace:Node1/@Error",
    }
    mock_input_action = "text_formatting"
    mock_input_data = {
        "namespace:Invoice": {
            "namespace:Node1": {
                "@Code": 7,
                "@Title": "ExampleTitle",
            },
        }
    }
    with pytest.raises(Exception):
        mapping.process_text_formatting(
            erronous_input_field, mock_input_action, mock_input_data
        )


def test_process_calculation_success():
    mock_input_data = {
        "namespace:Invoice": {
            "namespace:Node1": {
                "@Code": 7,
                "@Title": "ExampleTitle",
            },
        }
    }
    mock_calculation_field = "#namespace:Invoice/namespace:Node1/@Code + 15"
    expected_result = 22
    actual_result = mapping.process_calculation(
        mock_input_data, mock_calculation_field
    )

    assert expected_result == actual_result


def test_perform_nested_action_success():
    mock_input_data_1 = {
        "namespace:Invoice": {
            "@Argument1": "2023-12-31",
        }
    }
    mock_action_field_1 = {
        "path": "namespace:Invoice/@Argument1",
        "action": "as_is",
    }
    expected_result_1 = "2023-12-31"

    mock_input_data_2 = {
        "namespace:Invoice": {
            "namespace:Node1": {"@Code": 5, "@Title": "some_title"}
        }
    }
    mock_action_field_2 = {
        "action": "condition",
        "condition": "#namespace:Invoice/namespace:Node1/@Code == 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    }
    expected_result_2 = "some_title"

    mock_input_data_3 = {
        "namespace:Invoice": {
            "namespace:Node1": {
                "@Code": 5,
                "@Title": "ExampleTitle",
            },
        }
    }
    mock_action_field_3 = {
        "action": "text_formatting",
        "format_type": "uppercase",
        "path": "namespace:Invoice/namespace:Node1/@Title",
    }
    expected_result_3 = "EXAMPLETITLE"

    mock_input_data_4 = {
        "namespace:Invoice": {
            "namespace:Node1": {
                "@Code": 7,
                "@Title": "ExampleTitle",
            },
        }
    }
    mock_action_field_4 = {
        "expression": " 2 * ( ( 1 + 1 ) * ( 1 + 3 ) )",
        "action": "calc",
    }
    expected_result_4 = 16

    actual_result_1 = mapping.perform_nested_action(
        mock_input_data_1, mock_action_field_1
    )
    actual_result_2 = mapping.perform_nested_action(
        mock_input_data_2, mock_action_field_2
    )
    actual_result_3 = mapping.perform_nested_action(
        mock_input_data_3, mock_action_field_3
    )
    actual_result_4 = mapping.perform_nested_action(
        mock_input_data_4, mock_action_field_4
    )

    assert expected_result_1 == actual_result_1
    assert expected_result_2 == actual_result_2
    assert expected_result_3 == actual_result_3
    assert expected_result_4 == actual_result_4


def test_perform_nested_action_failure():
    mock_input_data = {}
    erronous_action_field = {
        "action": "error",
        "format_type": "uppercase",
        "path": "namespace:Invoice/namespace:Node1/@Title",
    }
    with pytest.raises(Exception):
        mapping.perform_nested_action(mock_input_data, erronous_action_field)

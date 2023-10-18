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
    pass


def test_process_condition_success():
    pass


def test_process_condition_failure():
    pass


def test_process_text_formatting_success():
    pass


def test_process_text_formatting_failure():
    pass


def test_process_calculation_success():
    pass


def test_perform_nested_action_success():
    pass


def test_perform_nested_action_failure():
    pass


def test_perform_nested_action_success():
    pass


def test_perform_nested_action_failure():
    pass

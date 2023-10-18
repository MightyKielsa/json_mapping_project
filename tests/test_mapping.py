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
    result = mapping.build_output_branch(mock_required_value, output_path_data)


def test_build_output_branch_failure():
    pass


def test_implement_output_branch_success():
    pass


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

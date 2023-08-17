import datetime

sample_schema = {
    "invoice_argument1": {
        "path": "namespace:Invoice/@Argument1",
        "action": "as_is",
    },
    "invoice_code": {
        "path": "namespace:Invoice/namespace:Node1/@Code",
        "action": "as_is",
    },
    "inv_complex_val": {
        "action": "datetime_formatting",
        "input_date": "#namespace:Invoice/@Argument1",
        "input_format": "%Y-%m-%d",
        "output_format": "%d-%m-%Y",
    },
    "inv_nested/some_val": {
        "path": "namespace:Invoice/namespace:Node1/@Code",
        "action": "as_is",
    },
    "inv_nested/some_other_val": {
        "path": "namespace:Invoice/namespace:Node1/@Title",
        "action": "as_is",
    },
    "inv_nested/something_nested/something_very_nested/yyy": {
        "path": "namespace:Invoice/namespace:Node1/@Title",
        "action": "as_is",
    },
    "inv_nested/something_something": {
        "path": "namespace:Invoice/namespace:Node1/@Code",
        "action": "as_is",
    },
    "inv_nested/something_nested/something_very_nested/xxx": {
        "path": "namespace:Invoice/namespace:Node1/@Title",
        "action": "as_is",
    },
    "conditional_value/inside_a_value": {
        "action": "condition",
        "condition": "3 < 5",
        "true": "namespace:Invoice/namespace:Node1/@Title",
        "false": "namespace:Invoice/namespace:Node1/@Code",
    },
}

sample_dict = {
    "namespace:Invoice": {
        "@xmlns:namespace": "http://www.example.com/xml/xml-ns/ExampleXML",
        "@Argument1": "2023-12-31",
        "namespace:Node1": {
            "@Code": "ExampleCode",
            "@Title": "ExampleTitle",
        },
        "namespace:Node2": {
            "namespace:NestedNode1": {
                "@some_arg": "somce_value",
                "namespace:NestedNode2": {
                    "namespace:RepearingNode": [
                        {
                            "@Caption": "ExampleCaption1",
                            "@Code": "ExampleCode1",
                            "@Value": "2023-01-01",
                        },
                        {
                            "@Caption": "ExampleCaption2",
                            "@Code": "ExampleCode2",
                            "@Value": "2023-12-31",
                        },
                    ]
                },
            }
        },
    }
}


def datetime_formatting(input_date, input_format="%d-%m-%y", output_format="%d/%m/%Y"):
    new_date = datetime.datetime.strptime(input_date, input_format).strftime(
        output_format
    )
    return new_date


def current_datetime(datetime_format="%Y-%m-%d %H:%M:%S"):
    now_datetime = datetime.datetime.now()
    return now_datetime.strftime(datetime_format)


def is_equal(value1, value2):
    return value1 == value2


def is_larger(value1, value2):
    return value1 > value2


def is_larger_or_equal(value1, value2):
    return value1 >= value2


def is_smaller_or_equal(value1, value2):
    return value1 <= value2


def is_smaller(value1, value2):
    return value1 < value2


def text_formatting():
    pass


actions = {
    "datetime_formatting": datetime_formatting,
    "current_datetime": current_datetime,
    "text_formatting": text_formatting,
    "==": is_equal,
    ">": is_larger,
    "<": is_smaller,
    ">=": is_larger_or_equal,
    "<=": is_smaller_or_equal,
}

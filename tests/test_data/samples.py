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
    "conditional_value/inside_a_value/inside_x": {
        "action": "condition",
        "condition": "#namespace:Invoice/namespace:Node1/@Code < 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    },
    "conditional_value/inside_a_value/inside_y": {
        "action": "condition",
        "condition": "#namespace:Invoice/namespace:Node1/@Code > 5",
        "true": "#namespace:Invoice/namespace:Node1/@Title",
        "false": "#namespace:Invoice/namespace:Node1/@Code",
    },
}

sample_dict = {
    "namespace:Invoice": {
        "@xmlns:namespace": "http://www.example.com/xml/xml-ns/ExampleXML",
        "@Argument1": "2023-12-31",
        "namespace:Node1": {
            "@Code": 7,
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

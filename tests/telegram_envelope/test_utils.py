from telegram_envelope import utils


def test_parse_command():
    assert utils.parse_command("") == ('', '')
    assert utils.parse_command("/hello") == ('hello', '')
    assert utils.parse_command("/command text") == ('command', 'text')
    assert utils.parse_command("/command and more text") == ('command', 'and more text')
    assert utils.parse_command("just simple text") == ('', 'just simple text')


def test_error_response():
    assert utils.error_response() == {
        'statusCode': 400,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': '""'
    }

    error = "Some error"
    assert utils.error_response(error) == {
        'statusCode': 400,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': f'"{error}"'
    }

    code = 500
    assert utils.error_response(status_code=code) == {
        'statusCode': code,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': '""'
    }

    content = 'application/json; charset=utf-8'
    assert utils.error_response(content_type=content) == {
        'statusCode': 400,
        'headers': {'Content-Type': content},
        'body': '""'
    }


def test_get_from_nested_dict():
    assert utils.get_from_nested_dict({}, {"a": ["some", "key"]}) == {"a": None}
    assert utils.get_from_nested_dict({"a": "some val"}, {"a": []}) == {"a": None}
    assert utils.get_from_nested_dict({"a": "some val"}, {}) == {}
    assert utils.get_from_nested_dict({"some": {"other": "thing"}}, {"a": ["some", "other"]}) == {"a": "thing"}
    assert utils.get_from_nested_dict({"some": {"other": "thing"}}, {"a": ["some", "other", "more"]}) == {"a": None}
    assert utils.get_from_nested_dict({"some": {"other": "thing"}}, {"a": ["some", "other", "more"]}, 0) == {"a": 0}
    assert utils.get_from_nested_dict({
        "k1": {"k11": "v1"},
        "k2": {
            "k22": {"k222": "v2"}
        },
        "k3": {},
        "k4": {
            "k44": {"too": "far"}
        },
        5: {
            True: 55.55
        }
    }, {
        "a1": ["k1", "k11"],
        "a2": ["k2", "k22", "k222"],
        "a3": ["k3"],
        "a31": ["k3", "another"],
        "a4": ["k4", "k44"],
        555: [5, True]
    }) == {"a1": "v1", "a2": "v2", "a3": {}, "a31": None, "a4": {"too": "far"}, 555: 55.55}

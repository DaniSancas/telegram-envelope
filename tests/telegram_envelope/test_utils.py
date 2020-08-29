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

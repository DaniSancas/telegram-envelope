import json
from typing import Tuple, Dict


def parse_command(text: str) -> Tuple[str, str]:
    """
    Parses a command + text from a text string.

    Given a string, it searches for a combination of command and text to
    split up those differentiated strings. Expected strings and results:

    ""                  -> ('', '')

    "/hello"            -> ('hello', '')

    "/command and text" -> ('command', 'and text')

    "just simple text"  -> ('', 'just simple text')

    :param text: Text to be parsed
    :type text: str
    :return: A tuple containing the command and the rest of the text
    :rtype: Tuple[str, str]
    """
    if text.startswith("/"):
        if " " in text:
            cmd, rest = text.split(" ", 1)
        else:
            cmd, rest = text, ''
        return cmd[1:], rest
    else:
        return '', text


def error_response(text: str = '', status_code: int = 400, content_type: str = 'text/html; charset=utf-8') -> Dict:
    """
    Creates an error response with parameterizable values.

    :param text: Optional explanatory error text
    :type text: str
    :param status_code: Response status code
    :type status_code: int
    :param content_type: Content type header
    :type content_type: str
    :return: Response dict with error status code
    :rtype: Dict
    """
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': content_type},
        'body': json.dumps(text)
    }

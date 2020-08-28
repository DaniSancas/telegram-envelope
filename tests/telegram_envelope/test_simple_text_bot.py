import json
from typing import Tuple
from telegram_envelope.simple_text_bot import WebHookTextBot, InputMessage


def run_simple_logic(input_message: InputMessage) -> Tuple[str, bool]:
    # Will behave normally
    if input_message.text == "/eco":
        return "ping", True
    return "pong", False


def run_exception_logic(input_message: InputMessage) -> Tuple[str, bool]:
    # Will throw an exception
    return str(1 / 0), True


def test_web_hook_text_bot_standard_message():
    input_message = InputMessage(789, "/eco", 456)
    request = {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "headers": {
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "body": "{\"update_id\":123,\n\"message\":{\"message_id\":456,\"from\":{\"id\":789,\"is_bot\":false,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"language_code\":\"en\"},\"chat\":{\"id\":789,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"type\":\"private\"},\"date\":1234567890,\"text\":\"/eco\",\"entities\":[{\"offset\":0,\"length\":4,\"type\":\"bot_command\"}]}}",
        "isBase64Encoded": False
    }
    web_hook_text_bot = WebHookTextBot(request)
    assert web_hook_text_bot.input_message.chat_id == input_message.chat_id
    assert web_hook_text_bot.input_message.text == input_message.text
    assert web_hook_text_bot.input_message.message_id == input_message.message_id

    execution = web_hook_text_bot.run(run_simple_logic)

    assert execution == {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'text': '"ping"',
                    'chat_id': web_hook_text_bot.input_message.chat_id,
                    'reply_to_message_id': 456
                }
            }


def test_web_hook_text_bot_case_edited_message():
    request = {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "headers": {
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "body": "{\"update_id\":123,\n\"edited_message\":{\"message_id\":456,\"from\":{\"id\":789,\"is_bot\":false,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"language_code\":\"en\"},\"chat\":{\"id\":789,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"type\":\"private\"},\"date\":1234567890,\"edit_date\":1234567890,\"text\":\"/eco2\",\"entities\":[{\"offset\":0,\"length\":5,\"type\":\"bot_command\"}]}}",
        "isBase64Encoded": False
    }
    web_hook_text_bot = WebHookTextBot(request)
    execution = web_hook_text_bot.run(run_simple_logic)

    assert execution == {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'},
                'body': {
                    'text': '"pong"',
                    'chat_id': web_hook_text_bot.input_message.chat_id
                }
            }


def test_web_hook_text_bot_case_wrong_request():
    request = {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "headers": {
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "body": "{\"something\": \"not expected\"}",
        "isBase64Encoded": False
    }
    web_hook_text_bot = WebHookTextBot(request)
    execution = web_hook_text_bot.run(run_simple_logic)

    assert execution == {
        'statusCode': 400,
        'headers': {'Content-Type': 'text/html; charset=utf-8'},
        'body': json.dumps("")
    }


def test_web_hook_text_bot_case_run_exception():
    request = {
        "resource": "/",
        "path": "/",
        "httpMethod": "POST",
        "headers": {
            "Accept-Encoding": "gzip, deflate",
            "Content-Type": "application/json",
            "X-Forwarded-Port": "443",
            "X-Forwarded-Proto": "https"
        },
        "body": "{\"update_id\":123,\n\"message\":{\"message_id\":456,\"from\":{\"id\":789,\"is_bot\":false,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"language_code\":\"en\"},\"chat\":{\"id\":789,\"first_name\":\"some\",\"last_name\":\"user\",\"username\":\"someuser\",\"type\":\"private\"},\"date\":1234567890,\"text\":\"/eco\",\"entities\":[{\"offset\":0,\"length\":4,\"type\":\"bot_command\"}]}}",
        "isBase64Encoded": False
    }
    web_hook_text_bot = WebHookTextBot(request)
    execution = web_hook_text_bot.run(run_exception_logic)

    assert execution == {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': {
            'text': '"An error occurred: division by zero"',
            'chat_id': web_hook_text_bot.input_message.chat_id
        }
    }

from typing import Tuple
from aws.simple_text_bot import WebHookTextBot, InputMessage


def run_simple_logic(input_message: InputMessage) -> Tuple[str, bool]:
    if input_message.text == "/eco":
        return "ping", True
    return "pong", False


def test_web_hook_text_bot():
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

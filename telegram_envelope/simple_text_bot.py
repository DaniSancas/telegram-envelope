import json
from typing import Optional, Tuple, Callable, Any, Dict
from telegram_envelope import utils


class InputMessage:
    def __init__(self, chat_id: int, text: str, message_id: int):
        """
        Constructor for InputMessage

        Initializes the values for chat_id, text and message_id
        as a simplified version of an incoming message.

        :param chat_id:
        :type chat_id: int
        :param text:
        :type text: str
        :param message_id:
        :type message_id: int
        """
        self.chat_id = chat_id
        self.text = text
        self.message_id = message_id


class WebHookTextBot:
    def __init__(self, http_request: Dict):
        """
        Constructor for WebHookTextBot

        Gets a simplified message from the incoming http request,
        or None if the expected data doesn't meet the requirements.

        :param http_request: Dictionary with the whole request
        :type http_request: Dict
        """
        self.input_message: Optional[InputMessage] = \
            self.get_input_message_from_http_request_dict(http_request)

    @staticmethod
    def get_input_message_from_http_request_dict(http_request: Dict) -> Optional[InputMessage]:
        """
        Get the input chat id, text and message id from an incoming message.

        Lookup for specific key-values in the dictionary and try to convert the id's to int.
        In case an expected key doesn't exist or an id is not convertible to int, None is returned.
        Otherwise, an InputMessage object is returned.

        :param http_request: Dictionary with the whole request
        :type http_request: Dict
        :return: None or InputMessage object with the input chat id, text and message id
        :rtype: Optional[InputMessage]
        """
        try:
            body_key = json.loads(http_request['body'])
            msg_key = body_key['message'] if 'message' in body_key else body_key['edited_message']
            chat_id = int(msg_key['chat']['id'])
            text = msg_key['text']
            message_id = int(msg_key['message_id'])

            return InputMessage(chat_id, text, message_id)
        except (KeyError, ValueError):
            return None

    def run(self, function: Callable[[InputMessage], Tuple[str, bool]]) -> Dict:
        """
        Executes an user provided function with the logic for the Telegram Bot.

        The function gets an InputMessage parameter, and returns a tuple with the output text message
        and a boolean telling if this response should appear to be replying to the incoming message.

        Then, a response dict is constructed with the return of the user provided function.

        :param function: An user provided function with the logic
        :type function: Callable[[InputMessage], Tuple[str, bool]]
        :return: Response dict
        :rtype: Dict
        """
        if self.input_message is None:
            return utils.error_response()
        else:
            try:
                text, is_reply = function(self.input_message)
            except Exception as e:
                text = f"An error occurred: {e}"
                is_reply = False

            response: Dict[str, Any] = {
                'statusCode': 200,
                'headers': {'Content-Type': 'application/json'}
            }
            body: Dict[str, Any] = {
                'method': 'sendMessage',
                'text': text,
                'chat_id': self.input_message.chat_id
            }

            # Add reply_to_message_id key-value in case is specified by the user provided function
            if is_reply:
                body['reply_to_message_id'] = int(self.input_message.message_id)

            response['body'] = json.dumps(body)

        return response

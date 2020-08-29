# Telegram Envelope

Micro-helper for AWS Telegram Bots written in Python

## What is the telegram-envelope project
It's a small Python library to manage requests and responses for Telegram Bots on AWS Lambda, invoked by web hooks through AWS Api Gateway.
 
It parses the incoming request in order to handle to the bot a simplified and digested request. It also manages the response creation, leaving out all the related boilerplate and allowing the developers to focus on their main task: the bot logic.

## How to use it

We strongly recommend to use [Serverless framework](https://www.serverless.com/) to create Telegram bots to work with [AWS Lambda](https://aws.amazon.com/lambda/).

Look at the ["Hello world" Python Serverless guide](https://www.serverless.com/framework/docs/providers/aws/examples/hello-world/python/) for more information. However, we'll collect here the important steps to use telegram-envelope.


### Create a serverless python project

Create it using something like this command `sls create --template aws-python --path my-project-name`

### Install the required dependencies

Create a `requirements.txt file`, write `telegram-envelope` on it and install the package via invoking `pip install -r requirements.txt`. You can find the package on it's [Pypi page](https://pypi.org/project/telegram-envelope/).

### Start using telegram-envelope package

On your `handler.py` file you'll find a `hello()` function. There's is where telegram-envelope package is going to be used. You can rename this function to another name (and also the `handler.py` file), but don't forget to change the reference later on the `serverless.yml` file.

We can use it this way. In this case we rename the `hello()` function to `app()` function, and we implement a function with our bot logic called `my_app_logic()`:

```python
from telegram_envelope.simple_text_bot import WebHookTextBot, InputMessage

def my_app_logic(input_message: InputMessage) -> (str, bool):
    """This is your telegram bot logic.

    It receives an InputMessage object. It contains:
    - input_message.chat_id (int): The id of the chat where the message comes from
    - input_message.text (str): The raw incoming text
    - input_message.message_id (int): The id of the incoming message (for us to decide to reply to it or not)
     
    It must return a tuple with:
    - A str: bot response text
    - A bool: whether to reply to the incoming message or not
    """
    return f"You said '{input_message.text}'", True


def app(event, context):
    """This is your entry point.
    
    We must initialize the WebHookTextBot with the raw event, 
    and then we can run our logic, handling a function with a specific 
    signature. See the my_app_logic() function above.
    """
    return WebHookTextBot(event).run(my_app_logic)
```

### Preparing to go live!

Once we developed our logic (and tested it!) we can make some tweaks to our `serverless.yml` file:

```yaml
# Welcome to Serverless!
#
# This file is the main config file for your service.
# It's very minimal at this point and uses default values.
# You can always add more config options for more control.
# We've included some commented out config examples here.
# Just uncomment any of them to get that config option.
#
# For full config options, check the docs:
#    docs.serverless.com
#
# Happy Coding!

service: my-project-name  # Change it with your project name

provider:
  name: aws
  runtime: python3.8

# you can overwrite defaults here
  stage: pro  # Your stage name (dev, test, prod...)
  region: eu-west-3  # Your deployment region on AWS

functions:
  myapp:  # Change it with your Lambda function name
    handler: handler.app # Change it with your `python file`.`python function`

plugins:
  - serverless-python-requirements

custom:
  pythonRequirements:
    dockerizePip: false
```

As you can see we are using a serverless plugin to package and ship our dependencies along with our telegram bot logic. You can read more about this plugin in the [official docs](https://www.serverless.com/blog/serverless-python-packaging).

Once all the steps are done, we can deploy our solution using `sls deploy`. Read more about [deploying our functions](https://www.serverless.com/framework/docs/providers/aws/guide/deploying/) and [deployment best practices](https://www.serverless.com/blog/serverless-deployment-best-practices/).

### And... That's all, folks!

We wish you a happy coding. If you have doubts, suggestions, improvements, share your experience or just want to say "Hi!" don't hesitate to contact us ^_^

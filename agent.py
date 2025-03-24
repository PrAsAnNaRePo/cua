import json
import os
from openai import OpenAI
from local_playwright import LocalPlaywrightComputer


class Agent:
    def __init__(
            self,
            system_prompt: str,
            headless: bool,
            starting_url: str,
            verbose: bool = True,
        ):
        self.system_prompt = system_prompt
        self.computer = LocalPlaywrightComputer(headless)
        self.starting_url = starting_url
        self.verbose = verbose

        if os.environ.get('OPENAI_API_KEY'):
            self.client = OpenAI(api_key=os.environ['OPENAI_API_KEY'])
        else:
            raise ValueError("openai api key missing...")

        self.message_hist = []

        self.computer.__enter__()
        if self.starting_url:
            self.computer.goto(self.starting_url if 'http' in self.starting_url else 'https://' + self.starting_url)

    def __handle_output(self, item):
        if item.type == "message":
            if self.verbose:
                print(item.content[0].text)

        elif item.type == "computer_call":
            action = item.action
            action_type = action.type
            action_args = {k: v for k, v in action if k != "type"}
            if self.verbose:
                print(f"==> {action_type}({action_args})")

            method = getattr(self.computer, action_type)
            method(**action_args)

            screenshot_base64 = self.computer.screenshot()
            
            # if user doesn't ack all safety checks exit with error
            pending_checks = item.pending_safety_checks

            call_output = {
                "type": "computer_call_output",
                "call_id": item.call_id,
                "acknowledged_safety_checks": pending_checks,
                "output": {
                    "type": "input_image",
                    "image_url": f"data:image/png;base64,{screenshot_base64}",
                },
            }
            return [call_output]
        
        return []
    
    def __create_response(self):
        response = self.client.responses.create(
            input=self.message_hist,
            tools=[
                {
                    "type": 'computer_use_preview',
                    "display_width": self.computer.dimensions[0],
                    "display_height": self.computer.dimensions[1],
                    "environment": self.computer.environment
                }
            ],
            truncation="auto",
            model="computer-use-preview",
        )

        return response

    def __call__(self, prompt):
        
        self.message_hist.append(
            {
                'role': 'user',
                'content': prompt
            }
        )

        response = self.__create_response()

        while True:

            self.message_hist += response.output

            fn_called = False
            for item in response.output:
                self.message_hist += self.__handle_output(item)
                
                if item.type!='message':
                    fn_called = True

            if fn_called:
                response = self.__create_response()
            else:
                break
            

agent = Agent(
    system_prompt="you are a browser agent who interacts with the browser.",
    headless=True,
    verbose=True
)

agent("go to apple store & check new m4 air")

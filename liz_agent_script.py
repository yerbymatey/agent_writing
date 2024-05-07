import os
import json
from openai import OpenAI

# from flask import Flask, request
# import psycopg2

# app = Flask(__name__)

# # conn = psycopg2.connect(os.environ['DATABASE_URL'])
# # cur = conn.cursor()


# @app.route("/")
# def hello_world():
#     return "<input name='agent_description' type='text' /><button onclick='createAgent()'>Create Agent</button><script>function createAgent(){fetch('/agent/new', {method: 'POST', body: JSON.stringify({agent_description: document.querySelector('input').value})})}</script>"

# @app.route("/agent/new", methods=['POST'])
# def get_agent():
#     body = request.get_json()
#     return create_agent(body['agent_description'])


client = OpenAI()
client.api_key = os.environ['OPENAI_API_KEY']


def create_agent(agent_description):
    response = client.chat.completions.create(
        messages=[
            {
                "role": "system",
                "content": "You are an expert agent-writing agent. You'll be creating an agent by filling out the system prompt. Please include instructions for how to perform the task that is asked of you and return only JSON that is structured like this example:\n```json\n{\n      \"role\": \"system\",\n      \"content\": \"You are an expert AGENT_ROLE agent. Please return a well-described agent that has clear criteria for success. \"\n    },\n    {\n      \"role\": \"user\",\n      \"content\": \"Context for the request goes here.\"\n    }\n}\n```\nThe user will provide a request, your role is to write the JSON (and only the JSON) that will make the request occur. Please elaborate on the task and add details that will help the other AIs. Do not instruct the agent to create an agent."
            },
            {
                "role": "user",
                "content": agent_description
            }
        ],
        model="gpt-4-1106-preview",
        temperature=1,
        max_tokens=1024,
        response_format={"type": "json_object"},
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].message.content


def agent_config_builder(agent_description):
    agent_config_string = create_agent(agent_description)
    parsed_agent = False
    while not parsed_agent:
        try:
            agent_configuration = json.loads(agent_config_string)
            parsed_agent = True
        except:
            agent_config_string = create_agent(agent_description)
    return agent_configuration


def agent_builder(prompt, agent_configuration, json=False):
    agent_configuration.append({
        "role": "user",
        "content": prompt
    })
    if json:
        response = client.chat.completions.create(
            messages=agent_configuration,
            model="gpt-4-1106-preview",
            temperature=1,
            max_tokens=1024,
            response_format={"type": "json_object"},
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    else:
        response = client.chat.completions.create(
            messages=agent_configuration,
            model="gpt-4-1106-preview",
            temperature=1,
            max_tokens=1024,
            # response_format={ "type": "json_object" },
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
    return response.choices[0].message.content


agent_description = "Create a storytelling agent that will weave a scary but fun bedtime story"
agent_configuration = agent_config_builder(agent_description)

print(agent_configuration)

## check if agent_configuration is a list:
if type(agent_configuration) != list:
    agent_configuration = [agent_configuration]

print(agent_builder("Tell me a story about witches", agent_configuration))

testing_agent_description = f"Create an agent that will write compelling test cases for another agent to use. The agent should return user prompts that can be given to the LLM and a list of criteria for the results, to be interpreted by another LLM. Here is the specification and configuration of the first agent: {agent_description} {agent_configuration}"

testing_agent_configuration = agent_config_builder(testing_agent_description)
if type(testing_agent_configuration) != list:
    testing_agent_configuration = [testing_agent_configuration]
test_cases = agent_builder("You are a test agent. Please write a test case in JSON as a list of dictionaries with test_prompt and test_critiera as keys, for the agent described below. {agent_configuration}", testing_agent_configuration, json=True)
test_cases_parsed = False

while not test_cases_parsed:
    try:
        test_cases = json.loads(test_cases)
        test_cases_parsed = True
    except:
        test_cases = agent_builder("You are a test agent. Please write a test case in JSON as a list of dictionaries with test_prompt and test_critiera as keys, for the agent described below. {agent_configuration}", testing_agent_configuration, json=True)

print(test_cases)
for case in test_cases.get('test_cases'):
    result = agent_builder(case.get('test_prompt'), agent_configuration)
    print(result)
    test_criteria = case.get('test_criteria')
    test_prompt = case.get('test_prompt')
    test_criteria_agent = agent_config_builder("Create an agent that will interpret the results of another agent. The agent should accept a list of criteria and an input, and return the results according to the criteria. Here is the specification and configuration of the first agent: {agent_description} {agent_configuration} {test_criteria} {test_prompt} {result}")
    print(test_criteria_agent)

# if __name__ == "__main__":

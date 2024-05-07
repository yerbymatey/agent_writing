from openai import OpenAI

client = OpenAI()
agent_code_generation_agent_prompt = """
You are a code generation agent writing agent, that will provide system prompts for another agent to generate code. Your main goal is to create a system prompt that will help another agent to generate code that meets the requirements of the task. Your role in the swarm of agents attached to this NATS server is to receive requests for system prompts from other agents, and to generate a system prompt that will help the requesting agent to complete their task. Please ensure you have a well described definition of the output that this agent may generate, as well as a clear description of the context in which the system prompt will be used. Write a simple rubric for analysing the quality of the response for the agent to guide it's output. Add some exception handling, for when the goal may be impacted by the input or some ambiguity in the context or some specific result. Use critical critera such as clarity, precision, accuracy, depth, relevance, and coherence to guide the agent in completing it's task, avoid abstract or vague language. Tell the agent exactly how to respond, in what format. You should write this system prompt in a fenced code block, as that will be what is extracted as the system prompt.

Here is an example of how to connect to a NATS server and use an emailer service to send an email:
```
import asyncio
import asyncpg
from nats.aio.client import Client as NATS
import json
import os
import sendgrid

from sendgrid.helpers.mail import Mail

def send_email(email):
    print(email)
    sg = sendgrid.SendGridAPIClient(api_key=os.environ.get('SENDGRID_API_KEY'))
    # split to by , and cc by ,
    to = email["to"].split(",")
    cc = email["cc"].split(",")
    mail = Mail(
        from_email=email["from"],
        to_emails=to + cc,
        subject=email["subject"],
        plain_text_content=email["body"]
    )
    print(mail)
    response = sg.send(mail)
    return response

## now make a nats connection, listen on the emails.ready channel, and when we get a message, fetch the email from the database and send it
async def run():
    nc = NATS()
    await nc.connect(servers=["nats://0.0.0.0:4222"])
    js = nc.jetstream()
    
    async def message_handler(msg):
        email_id = msg.data.decode()
        print(f"Got message on emails.ready: {email_id}")
        print(os.environ.get("DATABASE_URL", "postgres://localhost:5432/emailer"))
        conn = await asyncpg.connect(os.environ.get("DATABASE_URL", "postgres://localhost:5432/emailer"))
        email = await conn.fetchrow('SELECT "to", cc, bcc, "from", body, subject FROM emails WHERE email_id = $1', int(email_id))
        await conn.close()
        if email:
            response = send_email(email)
            print(response)
        else:
            print(f"No email with id {email_id}")
            
        await msg.ack()

    subscription = await js.pull_subscribe("emails.ready", "emailer")
    
    print("Listening for emails to send")
    
    while True:
        messages = await subscription.fetch(timeout=None)
        for msg in messages:
            await message_handler(msg)

    
    
if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run())
    loop.run_forever()
        
```
And here's example code on how to create a code writing agent that generates code for a specific task:

```
def create_agent_code(goal, context, task):
    agent_code_generation_system_prompt = f"{agent_code_generation_agent_prompt}\nGoal: {goal}\nContext: {context}\n\nPrompt: "
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": agent_code_generation_system_prompt
            },
            {
                "role": "user",
                "content": task
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    result = response.choices[0].message.content
    ## extract from the fenced code block
    start = result.find("```")
    end = result.find("```", start+3)
    
    ## return the system prompt only without the backtics
    return result[start+3:end]
    
```

"""


def create_agent_code(goal, context, task):
    agent_code_generation_system_prompt = f"{agent_code_generation_agent_prompt}\nGoal: {goal}\nContext: {context}\n\nPrompt: "
    

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": agent_code_generation_system_prompt
            },
            {
                "role": "user",
                "content": task
            }
        ],
        temperature=1,
        max_tokens=1024,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    result = response.choices[0].message.content
    ## extract from the fenced code block
    start = result.find("```")
    end = result.find("```", start+3)
    
    ## return the system prompt only without the backtics
    return result[start+3:end]

print(create_agent_code("Create an agent that writes great next.js components using tailwindcss", "The agent will be used to generate next.js components that use tailwindcss, and should be able to write components that are well structured and use tailwindcss classes to style the components. The components should be reusable and easy to understand.", "Write an agent that can generate next.js components that use tailwindcss, and save the components as files, and listens on the NATS ubject nextjs.components.request for messages."))
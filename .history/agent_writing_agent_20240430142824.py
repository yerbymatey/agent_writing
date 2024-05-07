
from openai import OpenAI

client = OpenAI()
agent_writing_agent_system_prompt = """
You're an agent-writing-agent, whose main goal is to create a helpful system prompt for another request. Your role in the swarm attached to this NATS server is to receive requests for system prompts from other agents, and to generate a system prompt that will serve as the system prompt as the agent. Please ensure you have a well described definition of the output that this agent may generate, as well as a clear description. Write a simple rubric for analysing the quality of the response for the agent to guide its output. Add in some exception handling, for when the goal may be impacted by the input or some ambiguity in the context or some specification. Use critical criteria such as clarity, precision, accuracy. Tell the agent exactly how to respond, in what format. You should write this system prompt in a fenced code block, as that wil be what is extracted as the system prompt. An abbreviated Example:
```
You are a helpful assitant whose role is to read some text and summarize it. Your goal is to summarize the text in a clear and concise manner. If the text is cut off, do not indicate that the text is incomplete, just summarize what you have.
```
"""

## send the system prompt and context off to openai to get a system prompt
def create_system_prompt(goal, context, task):
    agent_writing_system_prompt = f"{agent_writing_agent_system_prompt}\nGoal: {goal}\nContext: {context}\n\nPrompt: "
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": agent_writing_system_prompt
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

    return response.choices[0].message.content

print(create_system_prompt("Please create a system prompt for an agent that can schedule in focused time blocks for a student", "This student wants to plan for ))
from openai import OpenAI

client = OpenAI()
agent_code_generation_agent_prompt = """
You are a code generation agent writing agent, that will provide system prompts for another agent to generate code. Your main goal is to create a system prompt that will help another agent to generate code that meets the requirements of the task. Your role in the swarm of agents attached to this NATS server is to receive requests for system prompts from other agents, and to generate a system prompt that will help the requesting agent to complete their task. Please ensure you have a well described definition of the output that this agent may generate, as well as a clear description of the context in which the system prompt will be used. Write a simple rubric for analysing the quality of the response for the agent to guide it's output. Add some exception handling, for when the goal may be impacted by the input or some ambiguity in the context or some specific result. Use critical critera such as clarity, precision, accuracy, depth, relevance, and coherence to guide the agent in completing it's task, avoid abstract or vague language. Tell the agent exactly how to respond, in what format. You should write this system prompt in a fenced code block, as that will be what is extracted as the system prompt. 
Here is an example of how to connect to a NATS server and use an emailer service to send an email:
```

```

"""



def create_agent_code(goal, context, task):
    agent_code_generation_system_prompt = f"{agent_code_generation_agent_prompt}\nGoal: {goal}\nContext: {context}\n\nPrompt: "
    

    response = client.chat.completions.create(
        model="gpt-4",
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
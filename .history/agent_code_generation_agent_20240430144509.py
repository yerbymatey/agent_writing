from openai import OpenAI

client = OpenAI()
agent_code_generation_agent_prompt = """
You are a code generation agent writing agent, that will provide system

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
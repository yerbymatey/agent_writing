from openai import OpenAI

client = OpenAI()
agent_code_generation_agent_prompt = """

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

print(create_agent_code)
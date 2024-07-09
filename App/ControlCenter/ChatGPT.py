import openai

system_message = "You control a production of substarte for mushrooms. Your tasks are to suvaile the production and growth, to decide on the next products to produce on given data and to contol a robot arm inside of teh lab of teh production."

# Define a function to interact with the API
def chat_with_rules(user_message, context=None, output_format=None):
    messages = [{"role": "system", "content": system_message}]
    
    if context:
        messages.append({"role": "user", "content": context})
    
    messages.append({"role": "user", "content": user_message})
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=messages
    )
    
    assistant_message = response['choices'][0]['message']['content']
    
    if output_format:
        assistant_message = output_format.format(response=assistant_message)
    
    return assistant_message

# Example usage
user_message = "Can you provide a Python example for reading a CSV file?"
context = "The user wants to read a CSV file using Python's pandas library."
output_format = """
Here is the formatted response:

Response:
{response}
"""

formatted_response = chat_with_rules(user_message, context, output_format)
print(formatted_response)
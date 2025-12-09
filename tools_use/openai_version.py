#pip install openai
from openai import OpenAI
client = OpenAI()
import json

#having multiple tools
def get_weather(city: str):
    return {"city": city, "temp": "22°C", "condition": "Clear"}

def get_time(timezone: str):
    return {"timezone": timezone, "time": "14:32"}

def search_wikipedia(query: str):
    return {"query": query, "summary": "This is a demo summary."}

def calculate_distance(city1: str, city2: str):
    return {"city1": city1, "city2": city2, "distance_km": 450}

def convert_currency(amount: float, from_currency: str, to_currency: str):
    converted = amount * 1.1  # dummy conversion
    return {
        "amount": amount,
        "from": from_currency,
        "to": to_currency,
        "converted": converted
    }

#Declare Tools for the Model
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get real-time weather for a city.",
            "parameters": {
                "type": "object",
                "properties": {"city": {"type": "string"}},
                "required": ["city"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "get_time",
            "description": "Get current time in any timezone.",
            "parameters": {
                "type": "object",
                "properties": {"timezone": {"type": "string"}},
                "required": ["timezone"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Search Wikipedia and return summary.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculate_distance",
            "description": "Calculate distance in km between two cities.",
            "parameters": {
                "type": "object",
                "properties": {
                    "city1": {"type": "string"},
                    "city2": {"type": "string"},
                },
                "required": ["city1", "city2"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "convert_currency",
            "description": "Convert currency amounts.",
            "parameters": {
                "type": "object",
                "properties": {
                    "amount": {"type": "number"},
                    "from_currency": {"type": "string"},
                    "to_currency": {"type": "string"},
                },
                "required": ["amount", "from_currency", "to_currency"]
            }
        }
    }
]

#tool dispatcher
def call_tool(tool_name, tool_args):
    if tool_name == "get_weather":
        return get_weather(**tool_args)
    if tool_name == "get_time":
        return get_time(**tool_args)
    if tool_name == "search_wikipedia":
        return search_wikipedia(**tool_args)
    if tool_name == "calculate_distance":
        return calculate_distance(**tool_args)
    if tool_name == "convert_currency":
        return convert_currency(**tool_args)

    raise ValueError(f"Unknown tool: {tool_name}")


#LLM decides which tool to call
user_message = "How far is London from Paris?"

response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[{"role": "user", "content": user_message}],
    tools=tools,
    tool_choice="auto"
)

#exec the tool
message = response.choices[0].message

if message.tool_calls:
    tool_call = message.tool_calls[0]
    tool_name = tool_call.function.name
    tool_args = json.loads(tool_call.function.arguments)

    print("Model selected tool:", tool_name)

    # Run the correct tool using our dispatcher
    tool_result = call_tool(tool_name, tool_args)

#o/p result back to model
final_response = client.chat.completions.create(
    model="gpt-4.1",
    messages=[
        {"role": "user", "content": user_message},
        message,
        {
            "role": "tool",
            "tool_call_id": tool_call.id,
            "name": tool_name,
            "content": json.dumps(tool_result)
        }
    ]
)

print("Assistant:", final_response.choices[0].message.content)


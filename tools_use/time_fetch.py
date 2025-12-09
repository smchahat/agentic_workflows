import json
import display_functions
from dotenv import load_dotenv
_ = load_dotenv()

import aisuite as ai

# Create an instance of the AISuite client
client = ai.Client()

from datetime import datetime

def get_current_time():
    """
    Returns the current time as a string.
    """
    return datetime.now().strftime("%H:%M:%S")

get_current_time()
#'19:47:42'

'''
After defining your message structure you can construct your chat completion. This will make the LLM call for you and return the result. Let's take a look at the parameters in this call.

model: The model that will be used
messages: The list of messages passed to the LLM
tools: The list of tools that the LLM has access to
max_turns: This is the maximum amount of messages the LLM will be allowed to make. This can help prevent the LLM from getting into infinite loops and repeatedly calling a tool.
Run the cell below to call the LLM and see the response.
'''

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=messages,
    tools=[get_current_time],
    max_turns=5
)

# See the LLM response
print(response.choices[0].message.content)
#The current time is 19:43:26.
"""And just like that you've given your LLM access to tools! The aisuite tool turned your function into a tool that augmented the LLM's knowledge about the world."""

print(response)
#ChatCompletion(id='chatcmpl-CkxzhGJcJ4LdmUe9a2LH1CpCvHC7t', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='The current time is 19:43:26.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None), intermediate_messages=[ChatCompletionMessage(content='The current time is 19:43:26.', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)])], created=1765309741, model='gpt-4o-2024-08-06', object='chat.completion', service_tier='default', system_fingerprint='fp_37d212baff', usage=CompletionUsage(completion_tokens=12, prompt_tokens=70, total_tokens=82, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)), intermediate_responses=[])

"""
Manually defining tools

You saw that the docstring provided by our tool helped `aisuite` automatically turn your function into a tool for the LLM. This is very convenient. But what is happening behind the scenes to take your function and make it a tool?

Actually, what the tool looks like to the LLM is more complicated. Let's take a look at how the LLM is *actually* given a tool below. Like before, tools are given in a list. But in that list, the tools have set schema that they expect. Within this schema are several important parts:
* `name`: The name of the corresponding function that you defined locally
* `description`: A description that explains what the function does and is used by the LLM to help it decide when to use it
* `parameters`: If your function has parameters, they would also be described with the parameter name and a description of what the parameter should be.

Run the cell below to define your tool using the schema.
"""
tools = [{
    "type": "function",
    "function": {
        "name": "get_current_time", # <--- Your functions name
        "description": "Returns the current time as a string.", # <--- a description for the LLM
        "parameters": {}
    }
}]
"""
In this case where you define a schema, `aisuite` expects you to handle the execution. So you will not use `max_turns`, and instead handle the execution yourself. Let's set this up by defining the response.
"""

response = client.chat.completions.create(
    model="openai:gpt-4o",
    messages=messages,
    tools=tools, # <-- Your list of tools with get_current_time
    # max_turns=5 # <-- When defining tools manually, you must handle calls yourself and cannot use max_turns
)
print(json.dumps(response.model_dump(), indent=2, default=str))
"""
op- 
{
  "id": "chatcmpl-CkxzhGJcJ4LdmUe9a2LH1CpCvHC7t",
  "choices": [
    {
      "finish_reason": "stop",
      "index": 0,
      "logprobs": null,
      "message": {
        "content": "The current time is 19:43:26.",
        "refusal": null,
        "role": "assistant",
        "annotations": [],
        "audio": null,
        "function_call": null,
        "tool_calls": null
      },
      "intermediate_messages": [
        {
          "content": "The current time is 19:43:26.",
          "refusal": null,
          "role": "assistant",
          "annotations": [],
          "audio": null,
          "function_call": null,
          "tool_calls": null
        }
      ]
    }
  ],
  "created": 1765309741,
  "model": "gpt-4o-2024-08-06",
  "object": "chat.completion",
  "service_tier": "default",
  "system_fingerprint": "fp_37d212baff",
  "usage": {
    "completion_tokens": 12,
    "prompt_tokens": 70,
    "total_tokens": 82,
    "completion_tokens_details": {
      "accepted_prediction_tokens": 0,
      "audio_tokens": 0,
      "reasoning_tokens": 0,
      "rejected_prediction_tokens": 0
    },
    "prompt_tokens_details": {
      "audio_tokens": 0,
      "cached_tokens": 0
    }
  },
  "intermediate_responses": []
}
"""

"""
Notice that in the response you can see tool_calls under message. This response from the LLM is saying that the LLM now wants to call a tool, specifically, get_current_time. You can add some logic to handle this situation. Then pass that back to the model and get the final response.

Run the cell below to run the function locally and return it to the LLM and receive the final response.
"""

response2 = None

# Create a condition in case tool_calls is in response object
if response.choices[0].message.tool_calls:
    # Pull out the specific tool metadata from the response
    tool_call = response.choices[0].message.tool_calls[0]
    args = json.loads(tool_call.function.arguments)

    # Run the tool locally
    tool_result = get_current_time()

    # Append the result to the messages list
    messages.append(response.choices[0].message)
    messages.append({
        "role": "tool", "tool_call_id": tool_call.id, "content": str(tool_result)
    })

    # Send the list of messages with the newly appended results back to the LLM
    response2 = client.chat.completions.create(
        model="openai:gpt-4o",
        messages=messages,
        tools=tools,
    )

    print(response2.choices[0].message.content)

#The current time is 19:57:38.

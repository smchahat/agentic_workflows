import requests
import qrcode
from qrcode.image.styledpil import StyledPilImage


def get_weather_from_ip():
    """
    Gets the current, high, and low temperature in Fahrenheit for the user's
    location and returns it to the user.
    """
    # Get location coordinates from the IP address
    lat, lon = requests.get('https://ipinfo.io/json').json()['loc'].split(',')

    # Set parameters for the weather API call
    params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m",
        "daily": "temperature_2m_max,temperature_2m_min",
        "temperature_unit": "fahrenheit",
        "timezone": "auto"
    }

    # Get weather data
    weather_data = requests.get("https://api.open-meteo.com/v1/forecast", params=params).json()

    # Format and return the simplified string
    return (
        f"Current: {weather_data['current']['temperature_2m']}°F, "
        f"High: {weather_data['daily']['temperature_2m_max'][0]}°F, "
        f"Low: {weather_data['daily']['temperature_2m_min'][0]}°F"
    )

# Write a text file
def write_txt_file(file_path: str, content: str):
    """
    Write a string into a .txt file (overwrites if exists).
    Args:
        file_path (str): Destination path.
        content (str): Text to write.
    Returns:
        str: Path to the written file.
    """
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    return file_path


# Create a QR code
def generate_qr_code(data: str, filename: str, image_path: str):
    """Generate a QR code image given data and an image path.

    Args:
        data: Text or URL to encode
        filename: Name for the output PNG file (without extension)
        image_path: Path to the image to be used in the QR code
    """
    qr = qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H)
    qr.add_data(data)

    img = qr.make_image(image_factory=StyledPilImage, embedded_image_path=image_path)
    output_file = f"{filename}.png"
    img.save(output_file)

    return f"QR code saved as {output_file} containing: {data[:50]}..."

prompt = "Can you get the weather for my location?"

response = client.chat.completions.create(
    model="openai:o4-mini",
    messages=[{"role": "user", "content": (
        prompt
    )}],
    tools=[
        get_current_time,
        get_weather_from_ip,
        write_txt_file,
        generate_qr_code
    ],
    max_turns=5
)

display_functions.pretty_print_chat_completion(response)

"""
ChatCompletion(id='chatcmpl-CkyRmjAS9qyxNHnIIaspnUQRAWvx0', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Here’s the weather for your location:\nCurrent temperature: 48.2°F  \nHigh: 54.4°F  \nLow: 42.6°F', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None), intermediate_messages=[ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_NiRAE5VnUuk91Q64g5G7gG30', function=Function(arguments='{}', name='get_weather_from_ip'), type='function')]), {'role': 'tool', 'name': 'get_weather_from_ip', 'content': '"Current: 48.2\\u00b0F, High: 54.4\\u00b0F, Low: 42.6\\u00b0F"', 'tool_call_id': 'call_NiRAE5VnUuk91Q64g5G7gG30'}, ChatCompletionMessage(content='Here’s the weather for your location:\nCurrent temperature: 48.2°F  \nHigh: 54.4°F  \nLow: 42.6°F', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)])], created=1765311482, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=44, prompt_tokens=256, total_tokens=300, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)), intermediate_responses=[ChatCompletion(id='chatcmpl-CktXrS3gRcYNIKG2AP4EKFqoK2BbA', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_NiRAE5VnUuk91Q64g5G7gG30', function=Function(arguments='{}', name='get_weather_from_ip'), type='function')]))], created=1765292639, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=21, prompt_tokens=191, total_tokens=212, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))])
"""

prompt = "Can you make a txt note for me called reminders.txt that reminds me to call Daniel tomorrow at 7PM?"

response = client.chat.completions.create(
    model="openai:o4-mini",
    messages=[{"role": "user", "content": (
        prompt
    )}],
    tools=[
        get_current_time,
        get_weather_from_ip,
        write_txt_file,
        generate_qr_code
    ],
    max_turns=5
)

display_functions.pretty_print_chat_completion(response)

"""
ChatCompletion(id='chatcmpl-Ckte2at8j3nPjWpoktBcfgjgejPfn', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='I’ve created your note "reminders.txt" with the reminder to call Daniel tomorrow at 7PM. Let me know if you need any more notes or edits!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None), intermediate_messages=[ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_kLmVyQcvMJsDmcfzkqGuqppM', function=Function(arguments='{"file_path":"reminders.txt","content":"Remind me to call Daniel tomorrow at 7PM."}', name='write_txt_file'), type='function')]), {'role': 'tool', 'name': 'write_txt_file', 'content': '"reminders.txt"', 'tool_call_id': 'call_kLmVyQcvMJsDmcfzkqGuqppM'}, ChatCompletionMessage(content='I’ve created your note "reminders.txt" with the reminder to call Daniel tomorrow at 7PM. Let me know if you need any more notes or edits!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)])], created=1765293022, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=46, prompt_tokens=258, total_tokens=304, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)), intermediate_responses=[ChatCompletion(id='chatcmpl-Cktdzuc3bT1ZUjjaVMdci2Neml1ke', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_kLmVyQcvMJsDmcfzkqGuqppM', function=Function(arguments='{"file_path":"reminders.txt","content":"Remind me to call Daniel tomorrow at 7PM."}', name='write_txt_file'), type='function')]))], created=1765293019, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=234, prompt_tokens=205, total_tokens=439, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=192, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))])
"""

with open('reminders.txt', 'r') as file:
    contents = file.read()
    print(contents)

#Remind me to call Daniel tomorrow at 7PM.

prompt = "Can you make a QR code for me using my company's logo that goes to www.deeplearning.ai? The logo is located at `dl_logo.jpg`. You can call it dl_qr_code."

response = client.chat.completions.create(
    model="openai:o4-mini",
    messages=[{"role": "user", "content": (
        prompt
    )}],
    tools=[
        get_current_time,
        get_weather_from_ip,
        write_txt_file,
        generate_qr_code
    ],
    max_turns=5
)
print(response)
display_functions.pretty_print_chat_completion(response)
"""
ChatCompletion(id='chatcmpl-CkteMQGpn1uzV5qcqpROwGLK3gtD0', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='Your QR code has been generated and saved as dl_qr_code.png. It embeds your company logo and links to www.deeplearning.ai. Let me know if there’s anything else you need!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None), intermediate_messages=[ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_b3lF9rf4lCrfiOi7wTFWZPNQ', function=Function(arguments='{"data":"www.deeplearning.ai","filename":"dl_qr_code","image_path":"dl_logo.jpg"}', name='generate_qr_code'), type='function')]), {'role': 'tool', 'name': 'generate_qr_code', 'content': '"QR code saved as dl_qr_code.png containing: www.deeplearning.ai..."', 'tool_call_id': 'call_b3lF9rf4lCrfiOi7wTFWZPNQ'}, ChatCompletionMessage(content='Your QR code has been generated and saved as dl_qr_code.png. It embeds your company logo and links to www.deeplearning.ai. Let me know if there’s anything else you need!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)])], created=1765293042, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=53, prompt_tokens=293, total_tokens=346, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)), intermediate_responses=[ChatCompletion(id='chatcmpl-CkteGTG0CkfHoL3XjZF5FSEUAK0Gv', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_b3lF9rf4lCrfiOi7wTFWZPNQ', function=Function(arguments='{"data":"www.deeplearning.ai","filename":"dl_qr_code","image_path":"dl_logo.jpg"}', name='generate_qr_code'), type='function')]))], created=1765293036, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=492, prompt_tokens=223, total_tokens=715, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=448, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))])
"""

from IPython.display import Image, display

# Display image directly
Image('dl_qr_code.png')

prompt = "Can you help me create a qr code that goes to www.deeplearning.com from the image dl_logo.jpg? Also write me a txt note with the current weather please."

response = client.chat.completions.create(
    model="openai:o4-mini",
    messages=[{"role": "user", "content": (
        prompt
    )}],
    tools=[
        get_weather_from_ip,
        get_current_time,
        write_txt_file,
        generate_qr_code
    ],
    max_turns=10
)

print(response)
display_functions.pretty_print_chat_completion(response)
"""
ChatCompletion(id='chatcmpl-CkyPOhN0SiUKXWDuUtzRa5xkX1arD', choices=[Choice(finish_reason='stop', index=0, logprobs=None, message=ChatCompletionMessage(content='I’ve generated the QR code (saved as deeplearning_qr.png) linking to www.deeplearning.com with dl_logo.jpg embedded, and written your weather note in weather_note.txt:\n\n• QR code image: deeplearning_qr.png  \n• Text file: weather_note.txt  \n\nLet me know if you need anything else!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None), intermediate_messages=[ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_FBp0c9gbJjEO6qvB8syTS1tD', function=Function(arguments='{}', name='get_weather_from_ip'), type='function')]), {'role': 'tool', 'name': 'get_weather_from_ip', 'content': '"Current: 48.2\\u00b0F, High: 54.4\\u00b0F, Low: 42.6\\u00b0F"', 'tool_call_id': 'call_FBp0c9gbJjEO6qvB8syTS1tD'}, ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_ruOdKHGEqaA3sCW4jLH5zZUo', function=Function(arguments='{"data":"www.deeplearning.com","filename":"deeplearning_qr","image_path":"dl_logo.jpg"}', name='generate_qr_code'), type='function')]), {'role': 'tool', 'name': 'generate_qr_code', 'content': '"QR code saved as deeplearning_qr.png containing: www.deeplearning.com..."', 'tool_call_id': 'call_ruOdKHGEqaA3sCW4jLH5zZUo'}, ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_hC83inmZPLrUaaVpapmFvxR8', function=Function(arguments='{"file_path":"weather_note.txt","content":"Current weather: Current: 48.2°F, High: 54.4°F, Low: 42.6°F"}', name='write_txt_file'), type='function')]), {'role': 'tool', 'name': 'write_txt_file', 'content': '"weather_note.txt"', 'tool_call_id': 'call_hC83inmZPLrUaaVpapmFvxR8'}, ChatCompletionMessage(content='I’ve generated the QR code (saved as deeplearning_qr.png) linking to www.deeplearning.com with dl_logo.jpg embedded, and written your weather note in weather_note.txt:\n\n• QR code image: deeplearning_qr.png  \n• Text file: weather_note.txt  \n\nLet me know if you need anything else!', refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=None)])], created=1765311334, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=81, prompt_tokens=422, total_tokens=503, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)), intermediate_responses=[ChatCompletion(id='chatcmpl-CkteVjaMEateJFhMwg66Kt3Ey8abC', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_FBp0c9gbJjEO6qvB8syTS1tD', function=Function(arguments='{}', name='get_weather_from_ip'), type='function')]))], created=1765293051, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=725, prompt_tokens=218, total_tokens=943, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=704, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0))), ChatCompletion(id='chatcmpl-CkyPGCVoAf0pINOgdEBsWAczOYE1s', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_ruOdKHGEqaA3sCW4jLH5zZUo', function=Function(arguments='{"data":"www.deeplearning.com","filename":"deeplearning_qr","image_path":"dl_logo.jpg"}', name='generate_qr_code'), type='function')]))], created=1765311326, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=429, prompt_tokens=283, total_tokens=712, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=384, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0))), ChatCompletion(id='chatcmpl-CkyPMUwMWl03CoAw2mmWm3nPgfVGl', choices=[Choice(finish_reason='tool_calls', index=0, logprobs=None, message=ChatCompletionMessage(content=None, refusal=None, role='assistant', annotations=[], audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_hC83inmZPLrUaaVpapmFvxR8', function=Function(arguments='{"file_path":"weather_note.txt","content":"Current weather: Current: 48.2°F, High: 54.4°F, Low: 42.6°F"}', name='write_txt_file'), type='function')]))], created=1765311332, model='o4-mini-2025-04-16', object='chat.completion', service_tier='default', system_fingerprint=None, usage=CompletionUsage(completion_tokens=50, prompt_tokens=355, total_tokens=405, completion_tokens_details=CompletionTokensDetails(accepted_prediction_tokens=0, audio_tokens=0, reasoning_tokens=0, rejected_prediction_tokens=0), prompt_tokens_details=PromptTokensDetails(audio_tokens=0, cached_tokens=0)))])
🧠 LLM Action: get_weather_from_ip
{}
🔧 Tool Response: get_weather_from_ip
"Current: 48.2\u00b0F, High: 54.4\u00b0F, Low: 42.6\u00b0F"
🧠 LLM Action: generate_qr_code
{
  "data": "www.deeplearning.com",
  "filename": "deeplearning_qr",
  "image_path": "dl_logo.jpg"
}
🔧 Tool Response: generate_qr_code
"QR code saved as deeplearning_qr.png containing: www.deeplearning.com..."
🧠 LLM Action: write_txt_file
{
  "file_path": "weather_note.txt",
  "content": "Current weather: Current: 48.2\u00b0F, High: 54.4\u00b0F, Low: 42.6\u00b0F"
}
🔧 Tool Response: write_txt_file
"weather_note.txt"
✅ Final Assistant Message:
I’ve generated the QR code (saved as deeplearning_qr.png) linking to www.deeplearning.com with dl_logo.jpg embedded, and written your weather note in weather_note.txt: • QR code image: deeplearning_qr.png • Text file: weather_note.txt Let me know if you need anything else!

🧭 Tool Sequence:
get_weather_from_ip → generate_qr_code → write_txt_file
"""

### Final Takeaways

#- Tool calling lets LLMs go beyond text generation—they can now use functions as part of their reasoning.
#- Clear, well-documented functions (with precise docstrings) help the model know when and how to use each tool.
#- AISuite handles the complexity of translating python functions into tool schemas and orchestrating multi-step workflows.
#- Choosing the right model matters: smaller models are faster and cheaper for simple tasks, while stronger models are better for reasoning-heavy workflows.
#- Watching the conversation flow (prompts, tool calls, results, final response) is essential for debugging and improving agentic behaviors.

#With these elements in place, you now have the foundation to design agents that combine LLM reasoning with external tools to complete more complex tasks.

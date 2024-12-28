import requests
import os
import json
from typing import Dict, TypedDict, Annotated, Sequence
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('API_KEY')



def prompt_llm_completion(prompt):
    """
    Requests a prompt completion 
    Args:
        prompt_prefix (str): The prefix to add before the fetched content
        
    Returns:
        str: The text response from Lambda Labs,
        int: The total token usage count
    """
    if not api_key:
        raise ValueError("LAMBDA_API_KEY environment variable is not set")
    
    try:
        
        # Prepare the completion request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3.3-70b-instruct-fp8",
            "prompt": f"{prompt}",
            "temperature": 0
        }
        
        # Make the completion request
        completion_response = requests.post(
            "https://api.lambdalabs.com/v1/completions",
            headers=headers,
            json=data
        )
        completion_response.raise_for_status()
        
        resp_json = completion_response.json()

        return resp_json['choices'][0]['text'], resp_json['usage']['total_tokens']
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")

def prompt_llm_chat(messages):
    """
    Requests a prompt completion 
    Args:
        prompt_prefix (str): The prefix to add before the fetched content
        
    Returns:
        str: The text response from Lambda Labs,
        int: The total token usage count
    """
    # Ensure API key is set
    if not api_key:
        raise ValueError("LAMBDA_API_KEY environment variable is not set")
    
    try:
        
        # Prepare the completion request
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "llama3.3-70b-instruct-fp8",
            "messages": messages,
            "temperature": 0
        }
        
        # Make the completion request
        completion_response = requests.post(
            "https://api.lambdalabs.com/v1/chat/completions",
            headers=headers,
            json=data
        )
        completion_response.raise_for_status()
        
        resp_json = completion_response.json()

        return resp_json['choices'][0]['message'], resp_json['usage']['total_tokens']
        
    except requests.exceptions.RequestException as e:
        raise Exception(f"API request failed: {str(e)}")


class AgentNode(TypedDict):
    desc: str # Task description to be included in prompt
    prerequisites: list[str] # Prerequisite data needed before entering this node 
    success: str # Key in user_data that determines that this node has been filled
    acceptable: dict[str, str] # Values that we'll accept for our key.


# Define the state structure
class AgentState(TypedDict):
    messages: list[dict[str, str]]  # Conversation history
    user_data: dict[str, str]  # Patient data collected so far
    curr_node: AgentNode  # Current node task
    tasks : list[AgentNode]
    total_tokens: int


def parse_output(output: str) -> dict:
    json_str = '{' + output.split('{')[-1].split('}')[0] + '}'
    json_data = json.loads(json_str)
    return json_data

def format_acceptable(acceptable: dict) -> str:
    out = ''
    for k,v in acceptable.items():
        out += f"-'{k}': {v}.\n"

    return out

def format_conv(messages: dict) -> str:
    out = ''
    for m in messages:
        if m['role'] == 'system':
            continue
        else:
            out += f'{m['role']}: {m['content']}\n'
    return out



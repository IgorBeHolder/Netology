import requests
import time
import pandas as pd
import json
import numpy as np
import plotly.express as px

file_path = "/Users/velo1/SynologyDrive/GIT_syno/Mac/Netology/NLP/data/book-war-and-peace.txt"
max_tokens = '200'
approx_chars_per_token = 3
seq_len = 35000
res = []

# Read the content of the file
with open(file_path, 'r', encoding='utf-8') as file:
    long_text = file.read()

long_text = long_text[:seq_len]

def generate_context(approx_tokens, long_text):
    '''Function to generate a context of approximately the right number of tokens'''
    chars_for_tokens = approx_tokens * approx_chars_per_token
    return long_text[:chars_for_tokens]


def measure_llm_response_time(context_length, long_text):
    '''Function to measure the response time for a given context length'''
    context = generate_context(context_length, long_text)
    data = {
        "model": "/model-store/mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"content": "<s>[INST]You are a helpful assistant. Analyze the context and answer users question.[/INST]", "role": "system"},
            {"content": f"The context: {context}</s>", "role": "assistant"},
            {"content": "Try to count all the unique names in the conext. What are these names and their count? Try to do your best and make your answer as detailed as possible", "role": "user"}
        ],
        "max_tokens": f'{max_tokens}'
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }
    data_flush_cache = {
        "model": "/model-store/mistralai/Mistral-7B-Instruct-v0.1",
        "messages": [
            {"content": "<s>[INST]You are a helpful assistant. Analyze the context and answer users question.[/INST]", "role": "system"},
            {"content": f"The context: {context}</s>", "role": "assistant"},
            {"content": "Compose a dialog between Einstein and Ghandi?", "role": "user"}
        ],
        "max_tokens": "4096"
    }
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json'
    }    
    print(f"Context Length: {context_length} Tokens")

    start_time = time.time()
    response = requests.post('http://194.135.112.219:3003/v1/chat/completions', json=data, headers=headers)
    total_response_time = time.time() - start_time
    response_data = json.loads(response.text)
    usage_data = response_data['usage']
    completion_tokens = usage_data['completion_tokens']
    prompt_tokens = usage_data['prompt_tokens']

    # Flush the cache
    response = requests.post('http://194.135.112.219:3003/v1/chat/completions', json=data_flush_cache, headers=headers)
    return {
        'context_length': context_length,
        'max_tokens': max_tokens,
        'total_response_time': total_response_time,
        'completion_tokens': completion_tokens,
        'prompt_tokens': prompt_tokens,
        'real_tokens': usage_data
        # 'raw_payload': response.text

    }

# Function to run the experiment and save results to a dataframe
def run_experiment(long_text):
    '''Function to run the experiment and save results to a dataframe'''
    start_power = np.log10(200)
    end_power = np.log10(30000)
    context_lengths = np.logspace(start_power, end_power, num=7, dtype=int)    
    # context_lengths = [200, 500, 1000, 2000, 3000, 4000, 5000, 6000, 7000]
    results = []

    for length in context_lengths:
        result = measure_llm_response_time(length, long_text)
        results.append(result)
        print(f"Context Length: {result['context_length']} Tokens - Total: {result['total_response_time']:.4f} sec")

 
    return results

# Run the experiment and get the dataframe
for max_tokens in ['200', '1024', '2048', '4096']:
    print(f"Max Tokens: {max_tokens}{'*'*50}")
    res += run_experiment(long_text)

# Create a DataFrame from the results
df = pd.DataFrame(res)

# Display the dataframe
print(df)
df.to_csv('/Users/velo1/SynologyDrive/GIT_syno/Mac/Netology/NLP/LLM_resp_times_3090.csv', index=False)

# Plotting the data
fig = px.line(df, x='completion_tokens', y='total_response_time', color='prompt_tokens', title='Response Time vs Prompt Tokens. rtx3090')

# Showing the figure
fig.show()

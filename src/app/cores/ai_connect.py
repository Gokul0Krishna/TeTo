import ollama

def AI_response(query:str)-> str:
    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                'content': (
                    'You are an expert Linux sysadmin. Convert natural language'
                    ' instructions into concise, correct Bash commands only.'
                ),
            },
            {
                'role': 'user',
                'content': (
                    query
                ),
            },
        ],
    )

    return response['message']['content']
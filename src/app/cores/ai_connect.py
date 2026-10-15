import ollama

def _Ai_response(query:str,sytemprompt:str)-> str:
    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                   'content': (
                    sytemprompt
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



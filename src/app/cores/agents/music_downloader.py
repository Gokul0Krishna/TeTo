import ollama
from ai_tools import *
import ytdl
import json

def parse_task(user_query: str) -> dict:
    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "You are a task parser. Extract the URL and target file path from the user query. Return ONLY a valid JSON object with keys 'url' and 'filepath'."
                ),
            },
            {
                'role': 'user',
                'content': user_query,
            },
        ],
    )
    raw = response['message']['content']

    text = raw.content if hasattr(raw, "content") else str(raw)

    try:
        start = text.index("{")
        end = text.rindex("}") + 1
        return json.loads(text[start:end])
    except Exception as e:
        raise ValueError(f"Model did not return valid JSON:\n{text}") from e

def _path_resolver(file_path: str, available_paths: list[str]) -> dict:
    prompt = f"""
    You are a path matching assistant. 
    Target path requested by user: "{file_path}"
    
    Available existing paths on disk:
    {json.dumps(available_paths, indent=2)}

    Task:
    1. Compare the target path with the available paths. Check for exact matches or case-insensitive matches (e.g., "reports" vs "Reports").
    2. If a matching or highly similar existing path is found, return THAT existing path in WHOLE.
    3. If no matching or similar path exists, return the original target path so it can be created.

    Return ONLY a valid JSON object in this exact format:
    {{
      "resolved_path": "string",
      "exists": true or false,
      "action": "matched" or "create"
    }}
    """

    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[{"role": "user", "content": prompt}],
        format="json"
    )
    
    result = json.loads(response['message']['content'])
    return result

# fix the fucking files saving problem

def path_management_agent(user_target_path: str):
    available_paths = list_music_folders()
    decision = _path_resolver(user_target_path, available_paths)
    return decision

def music_downloader_agent(query: str) -> None:
    """
    Downloads music from the given URL and saves it to the specified output folder.
    """
    result = parse_task(query)
    if result and result['url'] and result['filepath']:
        file_path = path_management_agent(result['filepath'])
        music_download(result['url'], file_path['resolved_path'])
        return f"Music downloaded successfully to {file_path['resolved_path']}"
    else:
        return "Invalid query. Please provide a valid URL and target file path."

if __name__ == "__main__":
    music_downloader_agent("download this https://www.youtube.com/watch?v=dQw4w9WgXcQ and save it in /home/gokul/Music/test")
import json
import ollama
from tools import *

def parse_task(user_query: str) -> dict:
    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "You are a task parser. Extract the essay topic and target file path from the user query. Return ONLY a valid JSON object with keys 'essaytopic' and 'filepath'."
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


def generate_essay(essay_topic: str) -> str:
    response = ollama.chat(
        model='qwen2.5-coder:1.5b',
        messages=[
            {
                'role': 'system',
                'content': (
                    "You are an essay generator. Write a concise report on the given topic. Return ONLY the report text. No markdown, no explanation."
                ),
            },
            {
                'role': 'user',
                'content': essay_topic,
            },
        ],
    )
    raw = response['message']['content']

    text = raw.content if hasattr(raw, "content") else str(raw)
    return text


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

def path_management_agent(user_target_path: str):
    available_paths = list_college_folders()
    decision = _path_resolver(user_target_path, available_paths)
    return decision


def Agent1(user_query: str):
    task = parse_task(user_query)
    print("Parsed task:", task)
    if task and task['essaytopic'] and task['filepath']:
        essay = generate_essay(task['essaytopic'])
        print(essay)
        file_path = path_management_agent(task['filepath'])
        print(file_path)
        if essay and file_path:
            resolved_path = file_path['resolved_path']
            Create_pdf(essay, resolved_path+f"/{task['essaytopic'].replace(' ', '_')}.pdf")
            return f"Essay generated and saved to: {resolved_path}"
        else:
            return "Failed to generate essay or resolve file path."
    else:
        return "Invalid task format. Please provide both 'essaytopic' and 'filepath'."

if __name__ == "__main__":
    user_query = "Write a concise report on the impact of climate change on agriculture and save it to /collage/test/"
    result = Agent1(user_query)
    print("Agent1 result:", result)
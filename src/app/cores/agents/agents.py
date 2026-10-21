from smolagents import CodeAgent, LiteLLMModel, ToolCallingAgent, ChatMessage
import json
import ollama
model = LiteLLMModel(
    model_id="ollama_chat/qwen2.5-coder:1.5b",
    api_base="http://127.0.0.1:11434",
    num_ctx=8192,
)

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


# essay_agent = CodeAgent(
#     tools=[],
#     model=model,
#     max_steps=2,
#     instructions=(
#         "You are an essay generator. Use only the given topic. "
#         "Return ONLY the report text. No markdown, no explanation."
#     ),
# )

# folder_agent = ToolCallingAgent(
#     tools=[list_all_folder_paths],
#     model=model,
#     max_steps=4,
#     instructions=(
#         "Find candidate folders for the requested target path. "
#         "Call list_all_folder_paths once, then return ONLY paths, one per line. "
#         "If uncertain, return empty."
#     ),
# )

# pdf_agent = ToolCallingAgent(
#     tools=[Create_pdf],
#     model=model,
#     max_steps=3,
#     instructions="Use Create_pdf exactly as requested.",
# )


# def run_essay(topic: str) -> str:
#     return essay_agent.run(
#         f"Write a concise report on: {topic}. Include introduction, key events/themes, impact, and conclusion."
#     )


# def run_folder_search(target_path: str) -> str:
#     return folder_agent.run(f"List accessible folder paths and identify anything close to: {target_path}")


# def main(user_query: str):
#     task = parse_task(user_query)
#     print("Parsed task:", task)

#     with ThreadPoolExecutor(max_workers=2) as ex:
#         essay_future = ex.submit(generate_essay, task["essaytopic"])
#         folder_future = ex.submit(find_folders)

#         essay = essay_future.result()
#         folders = folder_future.result()

#     folder = resolve_folder(task["filepath"], folders)
#     pdf_path = os.path.join(folder, "report.pdf")

#     result = pdf_agent.run(
#         f'Call Create_pdf with filename "{pdf_path}" and content:\n{essay}'
#     )
#     print(result)

def Agent1(user_query: str):
    task = parse_task(user_query)
    print("Parsed task:", task)
    if task and task['essaytopic'] and task['filepath']:
        essay = generate_essay(task['essaytopic'])
        
    return essay 

if __name__ == "__main__":
    user_query = "Write a concise report on the impact of climate change on agriculture and save it to /home/user/reports/climate_report.pdf"
    result = Agent1(user_query)
    print("Agent1 result:", result)
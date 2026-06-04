from brain.qwen_subagent import dispatch_to_qwen

def dispatch_to_qwen_tool(task_description: str, context: str) -> str:
    return dispatch_to_qwen(task_description, context)

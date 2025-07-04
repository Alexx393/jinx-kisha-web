# apitools/custom_tools.py

def handle_custom_tool(prompt: str) -> str:
    """
    Recognize prompts like "tool: <tool_name> <args>".
    Implement your own tools here.
    """
    parts = prompt.split("tool:", 1)[-1].strip().split()
    if not parts:
        return "Specify a tool name after 'tool:'."
    tool_name = parts[0]
    args = parts[1:]

    # Example: a dummy calculator tool
    if tool_name == "calc":
        try:
            expr = " ".join(args)
            return str(eval(expr))
        except Exception as e:
            return f"Calc error: {e}"

    return f"Unknown tool `{tool_name}`. Available: calc."

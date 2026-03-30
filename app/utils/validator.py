VALID_ACTIONS = {"improve", "summarize", "ideas"}
def validate_action(action: str):
    if action not in VALID_ACTIONS:
        raise ValueError(f"Action must be one of {VALID_ACTIONS}")
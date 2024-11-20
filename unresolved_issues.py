# unresolved = []

# def add_to_unresolved(link):
#     global unresolved  # This is important!
#     if link not in unresolved:
#         unresolved.append(link)
#         print(f"Added link to unresolved: {link}")
#         return True
#     return False

# def get_unresolved():
#     global unresolved  # This is important!
#     return unresolved



import json

def load_unresolved():
    try:
        with open('unresolved.json', 'r') as f:
            data = json.load(f)
            # Ensure we always return a list
            return data if isinstance(data, list) else []
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_unresolved(unresolved):
    with open('unresolved.json', 'w') as f:
        json.dump(unresolved, f)

unresolved = load_unresolved()

def add_to_unresolved(link):
    global unresolved
    if not isinstance(unresolved, list):
        unresolved = []
    if link not in unresolved:
        unresolved.append(link)
        save_unresolved(unresolved)
        print(f"Added link to unresolved: {link}")
        
def remove_from_unresolved(link):
    global unresolved
    if link in unresolved:
        unresolved.remove(link)
        save_unresolved(unresolved)
        print(f"Removed link from unresolved: {link}")

def get_unresolved():
    global unresolved
    if not isinstance(unresolved, list):
        unresolved = load_unresolved()
    return unresolved
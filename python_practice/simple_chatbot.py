from datetime import datetime
from zoneinfo import ZoneInfo

def contains(terms, content):
    matches = []
    for term in terms:
        matches.append(term in content.lower())
    return any(matches)

# Test
# print(contains(['good morning', 'hello'], "Good morning sunshine!"))

def response(text):
    text = text.lower()
    if contains(['hello', 'hi', 'hey'], text):
        return "Hello!"
    elif contains(['time'], text):
        eastern_time = datetime.now(ZoneInfo("America/New_York"))
        return f"The time is {eastern_time.strftime('%I:%M %p %Z')}."
    elif contains(['encouraging words', 'motivation'], text):
        return "You matter, so go be great!"
    elif contains(['thanks', 'thank'], text):
        return "You're welcome!"
    else:
        return ("Have a great day! Goodbye!👋")


# Simple chat loop
while True:
    user_input = input("You: ")
    print(f'Bot: {response(user_input)}')
    
    if user_input.lower() in ['bye', 'exit', 'quit']:
        print("Bot: Goodbye! 👋")
        break

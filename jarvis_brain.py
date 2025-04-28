import openai
import json
import os


class JarvisBrain:
    def __init__(self, api_key, memory_file='jarvis_memory.json'):
        openai.api_key = api_key
        self.memory_file = memory_file
        self.memory = self.load_memory()
        self.chat_history = []

    def load_memory(self):
        if os.path.exists(self.memory_file):
            with open(self.memory_file, 'r') as file:
                return json.load(file)
        return {}

    def save_memory(self):
        with open(self.memory_file, 'w') as file:
            json.dump(self.memory, file, indent=4)

    def remember(self, key, value):
        self.memory[key] = value
        self.save_memory()

    def recall(self, key):
        return self.memory.get(key, "I don't remember that yet.")

    def ask(self, user_input):
        self.chat_history.append({"role": "user", "content": user_input})

        messages = [{"role": "system",
                     "content": "You're JARVIS, an intelligent, fun, human-like assistant who is friendly, helpful, and remembers things for your creator Om. You can talk like a best friend when needed."}]
        messages += self.chat_history[-5:]  # last 5 messages context

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # or gpt-4 if you have access
                messages=messages
            )
            reply = response['choices'][0]['message']['content']
            self.chat_history.append({"role": "assistant", "content": reply})
            return reply
        except Exception as e:
            return f"Oops, I had a problem thinking: {e}"

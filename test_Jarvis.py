from jarvis_brain import JarvisBrain

jarvis = JarvisBrain(api_key="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")

while True:
    user_input = input("You: ")

    if user_input.lower().startswith("remember"):
        try:
            _, key, value = user_input.split(" ", 2)
            jarvis.remember(key, value)
            print(f"Jarvis: Got it! I'll remember {key} = {value}")
        except:
            print("Jarvis: Use format: remember key value")
    elif user_input.lower().startswith("recall"):
        _, key = user_input.split(" ", 1)
        print(f"Jarvis: {jarvis.recall(key)}")
    else:
        reply = jarvis.ask(user_input)
        print("Jarvis:", reply)

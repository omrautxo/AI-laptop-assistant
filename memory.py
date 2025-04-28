# memory.py

memory_store = []


def remember(note):
    memory_store.append(note)


def recall_memory():
    if memory_store:
        return memory_store
    else:
        return ["You haven’t told me to remember anything yet."]

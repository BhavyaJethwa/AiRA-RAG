from langchain.memory import ConversationBufferMemory

_session_mem = {}

def get_memory_for_session(session_id: str):
    if session_id not in _session_mem:
        _session_mem[session_id] = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    return _session_mem[session_id]

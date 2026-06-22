


import os



os.environ["GOOGLE_API_KEY"] = "AQ.Ab8RN6KNFB90L8jk71tlkZkqtjFoH9IQ7Q9N68f26Y9iUY48ZA"

from langgraph.checkpoint.memory import MemorySaver



from langgraph.graph import StateGraph, START, END
from typing import TypedDict, Annotated
from langchain_core.messages import BaseMessage, HumanMessage


#now we are going to introduce a new reducer function like add operator this time we will use add messages because its specifically designed to store the previous chat messages like concatenation of list
from langgraph.graph.message import add_messages


class ChatState(TypedDict):
  messages: Annotated[list[BaseMessage], add_messages]

from langchain_google_genai import ChatGoogleGenerativeAI
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")
def chat_node(state : ChatState):

#take user query from state
  messages = state['messages']
#send it to llm
  response = llm.invoke(messages)
#response store state
  return {'messages' : [response]}

checkpointer = MemorySaver()
graph = StateGraph(ChatState)
graph.add_node('chat_node', chat_node)


graph.add_edge(START, 'chat_node')
graph.add_edge('chat_node', END)

chatbot = graph.compile(checkpointer = checkpointer)

chatbot

#initial_state = {
#   'messages' : [HumanMessage(content = 'hey i am vaibhav')]
#}
#config = {'configurable': {'thread_id': 'initial_chat_thread'}}
#chatbot.invoke(initial_state, config=config)

# --- ADD THIS GUARD BLOCK ---
if __name__ == "__main__":
    
    # --- INDENT ALL OF THIS BY ONE TAB ---
    current_thread_id = input('Enter unique session/thread ID: ').strip()

    while True:
        user_message = input('Type here: ')
        print ('User:', user_message)

        if user_message.strip().lower() in ['exit', 'quit', 'bye']:
            print("GOODBYE")
            break

        config = {'configurable': {'thread_id' : current_thread_id}}
        response = chatbot.invoke({'messages': [HumanMessage(content = user_message)]}, config = config)

        print('AI :', response['messages'][-1].content)
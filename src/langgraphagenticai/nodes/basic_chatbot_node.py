from src.langgraphagenticai.state.state import State

class BasicChatbotNode:
    """ Basic chatbot logic implementation. """

    def __init__(self, model):
        self.llm=model

    def process(self, state:State) -> dict:
        """ Process the input state and generate a graph """
        return {"messages": self.llm.invoke(state['messages'])}
    
    
from src.langgraphagenticai.state.state import State

class ChatbotWithToolNode:
    """
    Chatbot logic enhanced with tool integration.
    """
    def __init__(self, model):
        self.llm = model

    def process(self, state: State) -> dict:
        """
        Processes the input state and generates a response using the LLM with tool capabilities.
        """
        user_input = state["messages"][-1] if state["messages"] else ""
        llm_response = self.llm.invoke([{"role": "user", "content": user_input}])


        tool_response= f"Tool integration for: '{user_input}'"

        return {"messages": [llm_response, tool_response]}
    
    def create_chatbot(self, tools):
        """
        Initializes the chatbot with tool capabilities.
        """
        llm_with_tools = self.llm.bind_tools(tools)

        def chabot_node(state: State):
            """Chatbot logic for processing the input state and returning the response."""
            return {"messages": [llm_with_tools.invoke(state["messages"])]}
        
        return chabot_node
import streamlit as st
from langchain_core.messages import HumanMessage,AIMessage,ToolMessage
import json


class DisplayResultStreamlit:
    def __init__(self,usecase,graph,user_message):
        self.usecase= usecase
        self.graph = graph
        self.user_message = user_message

    def display_result_on_ui(self):
        usecase= self.usecase
        graph = self.graph
        user_message = self.user_message
        print(user_message)
        if usecase =="Basic Chatbot":
                for event in graph.stream({'messages':("user",user_message)}):
                    print(event.values())
                    for value in event.values():
                        print(value['messages'])
                        with st.chat_message("user", avatar="🧑‍💻"):
                            st.write(user_message)
                        with st.chat_message("assistant", avatar="🔮"):
                            st.write(value["messages"].content)

        elif usecase=="Chatbot with Web":
             # Prepare state and invoke the graph
            initial_state = {"messages": [user_message]}
            with st.spinner("Thinking and browsing the web... 🌐"):
                res = graph.invoke(initial_state)
            for message in res['messages']:
                if type(message) == HumanMessage:
                    with st.chat_message("user", avatar="🧑‍💻"):
                        st.write(message.content)
                elif type(message)==ToolMessage:
                    with st.chat_message("ai", avatar="🛠️"):
                        with st.expander("🔎 Tool Call", expanded=False):
                            st.write(message.content)
                elif type(message)==AIMessage and message.content:
                    with st.chat_message("assistant", avatar="🔮"):
                        st.write(message.content)

        elif usecase == "AI News":
            frequency = self.user_message
            name1=frequency.split(" ")[0]
            name2=frequency.split(" ")[1]
            name=f"{name1}_{name2}"
            # print(frequency)
            # print(name)
             # Prepare state and invoke the graph
            with st.spinner("Fetching and summarizing news... ⏳"):
                result = graph.invoke({"messages": frequency})
                try:
                    # Read the markdown file
                    AI_NEWS_PATH = f"./AINews/{name}_summary.md"
                    with open(AI_NEWS_PATH, "r") as file:
                        markdown_content = file.read()

                    # Display the markdown content in Streamlit
                    with st.container(border=True):
                        st.markdown(markdown_content, unsafe_allow_html=True)
                except FileNotFoundError:
                    st.error(f"News Not Generated or File not found: {AI_NEWS_PATH}", icon="🚫")
                except Exception as e:
                    st.error(f"An error occurred: {str(e)}", icon="⚠️")
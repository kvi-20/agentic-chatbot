### End to end Agentic AI Project

# End-to-End AI Chatbot

An end-to-end AI Chatbot project featuring multiple functionalities, including:  
- **Basic Chatbot**: Conversational AI capable of answering user queries.  
- **Web-Integrated Chatbot**: Chatbot accessible via a web interface using Streamlit.  
- **AI News Summarizer**: Summarizes the latest AI news from multiple categories such as Technology, Finance, Healthcare, and more.  

---

## Features

### 1. Basic Chatbot
- Handles general conversational queries.
- Maintains chat history for context-aware responses.

### 2. Chatbot with Web Interface
- User-friendly web UI built with **Streamlit**.
- Sidebar options for selecting **time frame** and **topic**.
- Chat interface supports interactive messaging.

### 3. AI News Summarizer
- Fetches the latest AI news based on user-selected **category**:
  - All, Healthcare, Finance, Technology, Education, Entertainment, Politics, Environment, Business
- Summarizes news into concise and readable format.
- Supports multiple time frames: Daily, Weekly, Monthly.

---

## Installation

1. Clone the repository:

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
```

2. Create a Conda environment:
```bash
conda create -n env python=3.12
conda activate env
```

3.  Install dependencies:
```bash
conda install --file requirements.txt
```

4.  Run the Web Chatbot
```bash
streamlit run app.py
```


Use the sidebar to select time frame and topic.

Click the Fetch Latest AI News button to get summarized AI news.

Chat with the bot in the main interface.

### Credits / Acknowledgements

This project was inspired and guided by [Krish Naik] through the course: https://www.udemy.com/course/complete-agentic-ai-bootcamp-with-langgraph-and-langchain/

##### License
This project is licensed under the MIT License.
from tavily import TavilyClient
from langchain_core.prompts import ChatPromptTemplate


class AINewsNode:
    def __init__(self,llm):
        """
        Initialize the AINewsNode with API keys for Tavily and GROQ.
        """
        self.tavily = TavilyClient()
        self.llm = llm
        # this is used to capture various steps in this file so that later can be use for steps shown
        self.state = {}

    def fetch_news(self, state: dict) -> dict:
        """
        Fetch AI news based on the specified frequency.
        
        Args:
            state (dict): The state dictionary containing 'frequency'.
        
        Returns:
            dict: Updated state with 'news_data' key containing fetched news.
        """
        # print(state)
        content = state['messages'][0].content.lower()
        # print(content)

        frequency, topic = content.split(" ")
        # frequency = frequncy.lower()
        self.state['frequency'] = frequency
        self.state['topic'] = topic
        print(frequency, topic)

        # frequency = state['messages'][0].content.lower()
        # self.state['frequency'] = frequency
        # topic = state['messages'][1].content.lower()
        # self.state['topic'] = topic

        time_range_map = {'daily': 'd', 'weekly': 'w', 'monthly': 'm', 'year': 'y'}
        days_map = {'daily': 1, 'weekly': 7, 'monthly': 30, 'year': 366}
        topic_map = {"all": "General", "healthcare": "healthcare", "finance": "finance", "technology": "technology",
                     "education": "education", "entertainment": "entertainment", "politics": "politics",
                     "environment": "environment", "business": "business"}

        response = self.tavily.search(
            query=f"Top {topic_map.get(topic)} news India and globally",
            topic="news",
            time_range=time_range_map[frequency],
            include_answer="advanced",
            max_results=20,
            days=days_map[frequency],
            # include_domains=["techcrunch.com", "venturebeat.com/ai", ...]  # Uncomment and add domains if needed
        )

        state['news_data'] = response.get('results', [])
        self.state['news_data'] = state['news_data']
        return state
    

    def summarize_news(self, state: dict) -> dict:
        """
        Summarize the fetched news using an LLM.
        
        Args:
            state (dict): The state dictionary containing 'news_data'.
        
        Returns:
            dict: Updated state with 'summary' key containing the summarized news.
        """

        news_items = self.state['news_data']

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", """Summarize news articles into markdown format. For each item include:
            - Date in **YYYY-MM-DD** format in IST timezone
            - Concise sentences summary from latest news
            - Sort news by date wise (latest first)
            - Source URL as link
            Use format:
            ### [Date]
            - [Summary](URL)"""),
            ("user", "Articles:\n{articles}")
        ])

        articles_str = "\n\n".join([
            f"Content: {item.get('content', '')}\nURL: {item.get('url', '')}\nDate: {item.get('published_date', '')}"
            for item in news_items
        ])

        response = self.llm.invoke(prompt_template.format(articles=articles_str))
        state['summary'] = response.content
        self.state['summary'] = state['summary']
        return self.state
    
    def save_result(self,state):
        frequency = self.state['frequency']
        topic = self.state['topic']
        name=f"{frequency}_{topic}"

        summary = self.state['summary']
        filename = f"./AINews/{name}_summary.md"
        with open(filename, 'w') as f:
            f.write(f"# {frequency.capitalize()} AI News Summary\n\n")
            f.write(summary)
        self.state['filename'] = filename
        return self.state
from __future__ import annotations

import os
from tavily import TavilyClient
from dotenv import load_dotenv

load_dotenv()


class TavilyResearcher:

    def __init__(self):
        self.client = TavilyClient(
            api_key=os.getenv("TAVILY_API_KEY")
        )

    def research_contact(self, name, organization, job_title):
        query = f"""
        {name}
        {organization}
        {job_title}
        longevity healthspan research
        """

        response = self.client.search(
            query=query,
            search_depth="advanced",
            max_results=5
        )

        results = response.get("results", [])

        research = "\n\n".join(
            [
                f"{r['title']}\n{r['content']}"
                for r in results
            ]
        )

        return research
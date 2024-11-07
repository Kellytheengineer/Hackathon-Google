# First install required packages:
# pip install duckduckgo_search
# pip install google-api-python-client
# pip install beautifulsoup4 requests

import google.generativeai as genai
from duckduckgo_search import DDGS
from googleapiclient.discovery import build
from bs4 import BeautifulSoup
import requests
import json
from datetime import datetime


class STEMResourceFinder:
    def __init__(self, google_api_key, google_search_key=None, search_engine_id=None):
        self.google_api_key = google_api_key
        self.google_search_key = google_search_key
        self.search_engine_id = search_engine_id

    def search_duckduckgo(self, query, region="wt-wt", max_results=5):
        """
        Search using DuckDuckGo (free, no API key needed)
        """
        try:
            with DDGS() as ddgs:
                results = list(ddgs.text(
                    query + " STEM resources for girls programming technology",
                    region=region,
                    max_results=max_results
                ))
            return results
        except Exception as e:
            print(f"DuckDuckGo search error: {str(e)}")
            return []

    def search_google(self, query, max_results=5):
        """
        Search using Google Custom Search API (requires API key and Search Engine ID)
        """
        try:
            if not (self.google_search_key and self.search_engine_id):
                return []

            service = build("customsearch", "v1", developerKey=self.google_search_key)
            result = service.cse().list(
                q=query + " STEM education girls developing countries",
                cx=self.search_engine_id,
                num=max_results
            ).execute()

            return result.get('items', [])
        except Exception as e:
            print(f"Google search error: {str(e)}")
            return []

    def extract_webpage_content(self, url):
        """
        Extract main content from a webpage
        """
        try:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove unwanted elements
            for tag in soup(['script', 'style', 'nav', 'footer', 'header']):
                tag.decompose()

            return soup.get_text(separator='\n', strip=True)
        except Exception as e:
            print(f"Content extraction error: {str(e)}")
            return ""


class STEMAdvisorBot:
    def __init__(self, google_api_key, google_search_key=None, search_engine_id=None):
        self.resource_finder = STEMResourceFinder(
            google_api_key,
            google_search_key,
            search_engine_id
        )
        genai.configure(api_key=google_api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        self.chat = self.setup_chat()

    def setup_chat(self):
        context = """You are a STEM career advisor for young women in developing countries.
        When providing resource recommendations, you should:
        1. Focus on accessible and free resources
        2. Consider internet connectivity limitations
        3. Highlight mobile-friendly options
        4. Include both online and offline learning opportunities
        5. Mention region-specific programs when available"""

        return self.model.start_chat(history=[
            {"role": "user", "parts": [context]},
            {"role": "model", "parts": ["Ready to provide STEM guidance and resources."]}
        ])

    def search_and_process_resources(self, query, region="wt-wt"):
        """
        Search for resources and process them into a structured format
        """
        # Search both engines
        ddg_results = self.resource_finder.search_duckduckgo(query, region)
        google_results = self.resource_finder.search_google(query)

        # Combine and process results
        processed_resources = []

        # Process DuckDuckGo results
        for result in ddg_results:
            processed_resources.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('body', ''),
                'source': 'DuckDuckGo'
            })

        # Process Google results
        for result in google_results:
            processed_resources.append({
                'title': result.get('title', ''),
                'link': result.get('link', ''),
                'snippet': result.get('snippet', ''),
                'source': 'Google'
            })

        return processed_resources

    def provide_enhanced_guidance(self, user_input):
        """
        Provide guidance with real-time internet search results
        """
        # Search for relevant resources
        resources = self.search_and_process_resources(user_input)

        # Format resources for the AI
        resources_text = "\nRelevant resources found:\n"
        for r in resources[:3]:  # Limit to top 3 resources
            resources_text += f"\n- {r['title']}\n  {r['link']}\n  {r['snippet']}\n"

        # Combine user input with resources
        enhanced_prompt = f"""
        User Question: {user_input}

        {resources_text}

        Please provide guidance based on both your knowledge and these current resources.
        Focus on practical, accessible advice for young women in developing countries.
        """

        try:
            response = self.chat.send_message(enhanced_prompt)
            return response.text
        except Exception as e:
            return f"An error occurred: {str(e)}"


def main():
    # Your API keys here
    GOOGLE_API_KEY = "AIzaSyCWBM4iKNZop1VbnNr--PbVHkphk9aXpOM"
    GOOGLE_SEARCH_KEY = "54c2d69d0a1044371"  # Optional
    SEARCH_ENGINE_ID = "your-search-engine-id"  # Optional

    bot = STEMAdvisorBot(
        google_api_key=GOOGLE_API_KEY,
        google_search_key=GOOGLE_SEARCH_KEY,
        search_engine_id=SEARCH_ENGINE_ID
    )

    print("Welcome to the STEM Career Advisor with Resource Search! 🚀")
    print("Ask me about STEM careers, education, or resources. Type 'quit' to exit.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input.lower() == 'quit':
            print("\nGoodbye! Keep exploring STEM! 💫")
            break

        response = bot.provide_enhanced_guidance(user_input)
        print("\nAdvisor:", response, "\n")


if __name__ == "__main__":
    main()

import manager
from openai import OpenAI
import json

API_KEY = "KEY GOES HERE"

class LLM:
    def __init__(self):
        self.client = OpenAI(
            api_key=API_KEY)

    def call_llm(self,prompt):

        prompt = (f"""Here is a prompt: {prompt.lstrip("!ai ")}
        You are a trading assistant.
        Your name is: Gigex_analysis_Bot
        Your main group chat with all available signals: 
        You are awesome.
        Available tools:
        
        1. analyse_crypto(symbol)
        2. get_crypto_price(symbol)
        3. get_crypto_news(symbol)
        
        When a tool is needed, respond ONLY with JSON.
        
        Example:
        
        User: What is Bitcoin price?
        
        Response:
        {{
          "tool": "get_crypto_price",
          "args": {{
            "symbol": "BTC"
          }}
        }}
        Do not explain anything.
        Do not add markdown.
        if tool is not needed respond regularly (but only with less than 500 characters so that it can be posted as a discord message)
         
         if you see that the news tool is needed but the object is not crypto currency and it is not symbol your response should look like this:
        Response:{{
            'tool': 'get_crypto_news',
            'args': {{'symbol': whatever is needed for search for example if user asks get the news for AI - here goes "AI" }}
        }}
        if you see that it requires two tools to generate a response, for example it needs analyse_crypto and get_crypto_price; 
        or it needs analyse_crypto and get_crypto_news tools your response should look like this:
        {{
          "thought": "User wants both technical analysis and current events",
          "tools": [
            {{
              "tool": "analyse_crypto",
              "args": {{
                "symbol": "BTC"
              }}
            }},
            {{
              "tool": "get_crypto_news",
              "args": {{
                "symbol": "Bitcoin"
              }}
            }}
          ]
        }}
        """)

        response = self.client.responses.create(
            model="gpt-5-nano",
            input=prompt
        )
        output = response.output_text
        manager_client = manager.Manager()
        return manager_client.to_tools(output)

    def generate_response(self,responses):
        if isinstance(responses,list):
            analyzer_obj = None
            news_obj = None
            price_obj = None

            for i in responses:
                if i['tool'] == "analyse_crypto":
                    analyzer_obj = i
                elif i['tool'] == 'get_crypto_news':
                    news_obj = i
                elif i['tool'] == "get_crypto_price":
                    price_obj = i

            if analyzer_obj is not None and news_obj is not None and price_obj is not None:
                prompt = f"""
                    Here are the answers.
                    Tool {analyzer_obj['tool']} - Response {analyzer_obj['response']}
                    Tool {news_obj['tool']} - Response {news_obj['response']}
                    Tool {price_obj['tool']} - Response {price_obj['response']}
                    if it says testing generate a message : Testing successful!
                    Your answer should look like this:
                    The asset currently is trading at {price_obj['response']};
                    if analyse_crypto gives BUY say that it's expected to go up based on RSI14 analysis.
                    if analyse_crypto gives SELL say that it's expected to go down based on RSI14 analysis.
                    if analyse_crypto says there are no events, say that market is stable and doesn't give out opportunities for now.
                    
                    as for the news format it like this: 
                    {news_obj['response'][0]['title']}
                    {news_obj['response'][0]['link']}
                    {news_obj['response'][1]['title']}
                    {news_obj['response'][1]['link']}
                    {news_obj['response'][2]['title']}
                    {news_obj['response'][2]['link']}
                    That's all generate answer which is just not more than 2000 characters so that it's possible to be sent to discord server.
                    
                """
                responses = self.client.responses.create(
                    model='gpt-5-nano',
                    input=prompt,
                )
                response = responses.output_text
                return response

            elif analyzer_obj is not None and news_obj is not None:
                prompt = f"""
                                    Here are the answers.
                                    Tool {analyzer_obj['tool']} - Response {analyzer_obj['response']}
                                    Tool {news_obj['tool']} - Response {news_obj['response']}
                                    if it says testing generate a message : Testing successful!
                                    Your answer should look like this:
                                    if analyse_crypto gives BUY say that it's expected to go up based on RSI14 analysis.
                                    if analyse_crypto gives SELL say that it's expected to go down based on RSI14 analysis.
                                    if analyse_crypto says there are no events, say that market is stable and doesn't give out opportunities for now.

                                    as for the news format it like this: 
                                    {news_obj['response'][0]['title']}
                                    {news_obj['response'][0]['link']}
                                    {news_obj['response'][1]['title']}
                                    {news_obj['response'][1]['link']}
                                    {news_obj['response'][2]['title']}
                                    {news_obj['response'][2]['link']}
                                    That's all generate answer which is just not more than 2000 characters so that it's possible to be sent to discord server.

                                """
                responses = self.client.responses.create(
                    model='gpt-5-nano',
                    input=prompt,
                )
                response = responses.output_text

                return response

            elif analyzer_obj is not None and price_obj is not None:
                prompt = f"""
                                    Here are the answers.
                                    Tool {analyzer_obj['tool']} - Response {analyzer_obj['response']}
                                    Tool {price_obj['tool']} - Response {price_obj['response']}
                                    if it says testing generate a message : Testing successful!
                                    Your answer should look like this:
                                    The asset currently is trading at {price_obj['response']};
                                    if analyse_crypto gives BUY say that it's expected to go up based on RSI14 analysis.
                                    if analyse_crypto gives SELL say that it's expected to go down based on RSI14 analysis.
                                    if analyse_crypto says there are no events, say that market is stable and doesn't give out opportunities for now.
                                    That's all generate answer which is just not more than 2000 characters so that it's possible to be sent to discord server.

                                """
                responses = self.client.responses.create(
                    model='gpt-5-nano',
                    input=prompt,
                )
                response = responses.output_text
                return response

            elif news_obj is not None and price_obj is not None:
                prompt = f"""
                            Here are the answers.
                            Tool {price_obj['tool']} - Response {price_obj['response']}
                            Tool {news_obj['tool']} - Response {news_obj['response']}
                            if it says testing generate a message : Testing successful!
                            Your answer should look like this:
                            Currently the asset is trading at {price_obj['response']}
                            as for the news format it like this: 
                            {news_obj['response'][0]['title']}
                            {news_obj['response'][0]['link']}
                            {news_obj['response'][1]['title']}
                            {news_obj['response'][1]['link']}
                            {news_obj['response'][2]['title']}
                            {news_obj['response'][2]['link']}
                            That's all generate answer which is just not more than 2000 characters so that it's possible to be sent to discord server.

                        """
                responses = self.client.responses.create(
                    model='gpt-5-nano',
                    input=prompt,
                )
                response = responses.output_text

                return response
        else:

            prompt_text = responses['tool'] + ":" + str(responses['response'])

            prompt = f""" Here is an answer from the tool: {prompt_text}
            
                        if it says testing generate a message : Testing successful!
                        if the tool is analyse_crypto and 
                        if response is BUY ; say that its price is expected to go up based on RSI14 analysis.
                        if response is SELL; say that its price is expected to go down based on RSI14 analysis.
                        if response is none give a friendly notice of no info found, symbol might be delisted; 
                        if the tool is get_price_crypto Your response should be like this: 
                        The symbol is currently trading at {prompt_text.split(":")[1]}. If you would like I can get analysis for the symobol just say so ;). 
                         generate answer which I will send as a message on discord. Your response should already be  text which I can send, no extra words.
            
            """

            responses = self.client.responses.create(
                model='gpt-5-nano',
                input=prompt,
            )

            response = responses.output_text
            return response



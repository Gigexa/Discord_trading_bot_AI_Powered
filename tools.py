import manager
import analyser
import json



class Tools:
    def __init__(self):
        self.tools = {"analyse_crypto":self.analyse_crypto,
                      "get_crypto_news":self.get_crypto_news,
                      "get_crypto_price":self.get_crypto_price}


    def check_tool(self,content):
        try:
            if content['tool'] in self.tools:
                response = {'tool': content['tool'],
                            'response' : self.tools[content['tool']](content['args']['symbol'])}
                manager_client = manager.Manager()
                return manager_client.to_llm_response(response)

            else:
                pass
        except KeyError as e:
            responses = []
            for i in content['tools']:
                response = self.tools[i['tool']](i['args']['symbol'])
                responses.append({'tool': i['tool'], "response":response})

            manager_client = manager.Manager()
            return manager_client.to_llm_response(responses)


    def analyse_crypto(self,symbol):
        analysis = analyser.Analyzer(symbol = f"{symbol}-USD", period = '5d', interval = '1h')
        response = analysis.analyze()
        return response

    def get_crypto_news(self,symbol):
        manager_client =  manager.Manager()
        return manager_client.to_rag(symbol)


    def get_crypto_price(self,symbol):
        analysis = analyser.Analyzer(symbol = f"{symbol}-USD", period = '5d', interval = '1h')
        response = analysis.get_price()
        return response

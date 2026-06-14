
import llm
import tools
import rag
import json



class Manager:

    def to_llm(self,content):
        llm_client = llm.LLM()
        return llm_client.call_llm(content)

    def to_llm_response(self,content):
        llm_client = llm.LLM()
        return llm_client.generate_response(content)

    def to_tools(self,content):
        try:
            content = json.loads(content)
            tools_client = tools.Tools()
            return tools_client.check_tool(content)
        except json.decoder.JSONDecodeError as e:
            print(e)
            return "We are unable to decode the message, please generate new prompt!"


    def to_rag(self,content):
        rag_client = rag.RAG()
        return rag_client.get_news(content)



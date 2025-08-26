from langchain_core.documents import Document


class PromptGenService:
    def __init__(self):
        pass
    def generatePrompt(self , input_query : str , documents: list[Document])->str:
        return self.__prepareContext__(input_query , documents)
    def __prepareContext__(self , input_query:str , documents : list[Document])->str:
        return f'''You are an expert Text-to-SQL model.
        Your task is to generate a single, correct SQL query that answers the user's question, based on the provided database schema.
        Do not include any explanations, just the SQL query itself.
        
        ### Context
        {'\n'.join([f' - {self.prep_doc(doc)}' for doc in documents])}

        ### User Question
        {input_query}

        ### Generated SQL Query
        '''
    def __prepDocumentContext__(self , docuemnt:Document)->str:
        return (
            f"Question: {docuemnt.metadata['prompt']}\n"
            f"Database Schema: {docuemnt.metadata['schema_context']}\n"
            f"Sql Query: {docuemnt.metadata['sql_query']}\n"
            f"Domain: {docuemnt.metadata['domain']}\n"
        )
    def prep_doc(self , item:Document):
        return (
                f"Question: {item.metadata['prompt']}\n"
                f"Database Schema: {item.metadata['schema_context']}\n"
                f"Sql Query: {item.metadata['sql_query']}\n"
                f"Domain: {item.metadata['domain']}\n"
            )
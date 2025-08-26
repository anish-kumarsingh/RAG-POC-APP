from huggingface_hub import InferenceClient

class GeneratorService:
    def __init__(self, model_id:str):
        self.client = InferenceClient()
        self.model_id = model_id
        pass
    def generateResponse(self , input_query:str , instruction_prompt:str):
        completion = self.client.chat.completions.create(
        model=self.model_id,
        messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': input_query},
                ],
            )
        print('==============Response from OpenAI Model========\n')
        print(completion.choices[0].message)
        print('==============END of Response from OpenAI Model========\n')
        return completion.choices[0].message
    
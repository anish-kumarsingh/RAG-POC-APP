from huggingface_hub import InferenceClient
import logging

logger = logging.getLogger(__name__)

class GeneratorService:
    _instance=None
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self, model_id:str):
        if not hasattr(self , '_initialized'):
            self.client = InferenceClient()
            self.model_id = model_id
            self._initialized=True
        pass
    def generateResponse(self , input_query:str , instruction_prompt:str):
        completion = self.client.chat.completions.create(
        model=self.model_id,
        messages=[
                {'role': 'system', 'content': instruction_prompt},
                {'role': 'user', 'content': input_query},
                ],
            )
        logger.info('==============Response from OpenAI Model========\n')
        logger.info(completion.choices[0].message)
        logger.info('==============END of Response from OpenAI Model========\n')
        return completion.choices[0].message
    
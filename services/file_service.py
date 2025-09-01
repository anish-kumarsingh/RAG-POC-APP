import logging

class FileService:
    _instance=None
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    def __init__(self):
        if not hasattr(self , '_initialized'):
            self._initialized=True
            self.logger= logging.getLogger(__name__)
            self.logger.info("Initialized File Service.")
        pass
    def loadTextFile(self , path:str)->str:
        content = None
        try:
            with open(path , 'r') as file:
                content = file.read()
        except Exception as ex:
            self.logger.error(f"Error while reading file : {path}", ex)
        return content
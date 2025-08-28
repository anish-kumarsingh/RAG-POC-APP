from jproperties import Properties

props_instances = {}

class PropLoader:
    def __init__(self, path:str):
        if path not in props_instances:
            self.properties=Properties()
            with open(path ,'rb') as props:
                self.properties.load(props, 'utf-8')
            props_instances.setdefault(path , self.properties)
            print(props_instances.items())
        else :
            self.properties = props_instances.get(path)
        print(self.properties)
        pass
    def getProp(self , prop_key:str):
        map = self.properties.get(prop_key)
        if map is not None:
            return map.data
        else :
            return None

class SmartSchema(object):
    
    def __init__(self, defination):
        self.defination = defination
    
    def invoke(self, instance, itter=10):
        for key, value in self.defination.items():
            if key not in instance:
                try:
                    instance[key] = value(instance)
                except KeyError as keyIssue:
                    print("key {} not found, error raised: {}".format(key, keyIssue))
                    continue
        if  not set(self.defination).issubset(set(instance)) and itter:
            self.invoke(instance, itter - 1)



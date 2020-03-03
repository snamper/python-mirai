class Depend:
    def __init__(self, func, middlewares=[]):
        self.func = func
        self.middlewares = middlewares
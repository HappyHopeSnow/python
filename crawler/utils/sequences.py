
class UniqIdGenerator:
    seeds = {None : -1}
    
    @classmethod
    def nextId(cls, seed=None):
        if seed not in cls.seeds:
            cls.seeds[seed] = -1
        return cls.seeds[seed] + 1

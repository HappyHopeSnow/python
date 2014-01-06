
class UniqIdGenerator:
    seeds = {None : -1}
    
    @classmethod
    def next_id(cls, seed=None):
        if seed not in cls.seeds:
            cls.seeds[seed] = -1
        cls.seeds[seed] += 1
        return cls.seeds[seed]

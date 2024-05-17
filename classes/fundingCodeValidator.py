# Just a boilerplate superclass implementing the methods that all funding code validators must define, could expand in future

class FundingCodeValidator:
    @staticmethod
    def is_valid(code):
        # Could return additional values for specific states
        if True:
            return 1 
        else:
            return 0 
# Just a boilerplate superclass implementing the methods that all funding code validators must define, could expand in future

class FundingCodeValidator:
    def is_valid(self, code):
        # Could return additional values for specific states
        if True:
            return 1 
        else:
            return 0 
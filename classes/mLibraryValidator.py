import re
from classes.fundingCodeValidator import FundingCodeValidator

class MLibraryValidator(FundingCodeValidator):
    @staticmethod
    def is_valid(code):
        if looks_external_chartfield(code):
            return 0 
        else:
            return 1

    @staticmethod
    def looks_external_chartfield(code):
        # Checks for codes that appear to be external chartfield codes
        chartfield = re.compile('(\d){2}[ -](\d){5}[ -](\d){4}[ -](\d){5}[ -](\d){5}')
        return chartfield.match(code)
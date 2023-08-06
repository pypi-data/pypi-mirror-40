import re

class RegexHunter: 
    
    # Sniff any email adress:
    def sniff_emails(self, data):        
        return re.findall(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+", data)
    
    # Sniff Phones
    def sniff_phones(self, data, phone_format="all"):        
        phone_regex = {
            'fr': r"(?:\+33|06|07)(?:\s|\.|-)\d{1,2}(?:(?:\s|.|-)\d{2}){3,4}",
            'us': r"(?:\(\d{3}\)|\d{3}-)(?:\s|\.|-|\d)\d{2,3}(?:\s|\.|-)\d{4}",
            'int': r"\+\d{1,3}(?:(?:-|\.|\s)\d{3,4}){3,4}"
        }
        
        phone_regex['all'] = re.compile("(%s|%s|%s)" % (phone_regex['fr'], phone_regex['us'], phone_regex['int']))
        
        if phone_format not in phone_regex.keys():
            print('Wrong format, check out available ones:\n{}'.format(list(phone_regex.keys())))
        else:        
            return re.findall(phone_regex[phone_format], data)
    
    # Sniff postal code
    def sniff_cp_zip(self, data):
        return re.findall(r"\D(\d{5})\D", data)
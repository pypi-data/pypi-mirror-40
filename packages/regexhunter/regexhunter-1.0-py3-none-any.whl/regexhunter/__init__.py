__author__ = "Tom Moritz"
__doc__="""
==========================================================
                      REGEX HUNTER
==========================================================
This library is based on the re library.
Import the class Hunter from regexhunter then you can use:
sniff_emails(data)
sniff_phones(data, phone_format) with phone_format['fr', 'us', 'int', 'all']
sniff_cp_zip(data)
All of theses functions return an array of matching elements.
"""

import RegexHunter
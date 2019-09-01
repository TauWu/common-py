# -*- coding: utf-8 -*-
# URL Parser

from urllib.parse import parse_qs

class URLParser(object):

    def __init__(self, str_value):
        self.str_value = str_value

    def parse(self):
        return parse_qs(self.str_value, keep_blank_values=False)

    def parse_with_blank(self):
        return parse_qs(self.str_value, keep_blank_values=True)

    def get_item(self, item_key):
        res = self.parse()
        return res.get(item_key, [])

if __name__ == "__main__":
    
    obj = URLParser("red=5&green=&blue=sad")
    print(obj.parse())
    print(obj.parse_with_blank())
    print(obj.get_item("red"))
    print(obj.get_item("black"))

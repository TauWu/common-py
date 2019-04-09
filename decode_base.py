# -*- coding: utf-8 -*-
# Translate from &#x1234 or &#12314 to Chinese.

import re

# Turn &#xxxx; to char.
def _dec_ascii_to_str(ascii_match):
    ascii_data = re.findall(r"[0-9]+", ascii_match.group())[0]
    return chr(int(ascii_data, 10))

def _dec_html_to_str(html):
    cpl = re.compile(r"&#[0-9]+;")
    html = re.sub(cpl, _dec_ascii_to_str, html)
    return html

def _hex_ascii_to_str(ascii_match):
    ascii_data = re.findall(r"[0-9A-Z]+", ascii_match.group())[0]
    return chr(int(ascii_data, 16))

def _hex_html_to_str(html):
    cpl = re.compile(r"&#x[0-9A-Z]+;")
    html = re.sub(cpl, _hex_ascii_to_str, html)
    return html

def html_to_str(html, ascii_type: type=object) -> str:
    '''html_to_str
    You can give ascii_type or it will try dec and hex code.

    '''
    if ascii_type == hex:
        return _hex_html_to_str(html)

    elif ascii_type == int:
        return _dec_html_to_str(html)

    elif ascii_type == object:
        return _hex_html_to_str(_dec_html_to_str(html))

    else:
        raise TypeError(f"Unsupport type of ascii_type: {ascii_type}")

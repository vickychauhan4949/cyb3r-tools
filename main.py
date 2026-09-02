from flask import Flask, request
import hashlib, base64, random, string, re
from urllib.parse import quote, unquote, urlparse, parse_qs
import html

app = Flask(__name__)
visitors = 1301

TOOLS = ["MD5","SHA256","Base64 Encode","Base64 Decode","Uppercase","Lowercase","Reverse","Word Count","Password Gen","Name Style - 20 Fonts","UPI QR Generator","Fake Link Check","Phone Info","YouTube Thumb","Insta Guide","URL Encode","URL Decode","Binary","Email Check","IP Info"]

def fancy_20(t):
    # IG 20 Fonts
    t_low = t.lower()
    def circled(txt):
        return ''.join(chr(0x24D0 + ord(c)-97) if 'a'<=c<='z' else c for c in txt.lower())
    def fullwidth(txt):
        return ''.join(chr(0xFF21 + ord(c)-97) if 'a'<=c<='z' else c for c in txt.lower())
    
    fonts = []
    fonts.append(f"1. Bold: {t.upper()}")
    fonts.append(f"2. Circled: {circled(t)}")
    fonts.append(f"3. Fullwidth: {fullwidth(t)}")
    fonts.append(f"4. Leet: {t.replace('a','4').replace('e','3').replace('i','1').replace('o','0').replace('s','$')}")
    fonts.append(f"5. Reverse: {t[::-1]}")
    fonts.append(f"6. Upper Lower: {''.join(c.upper() if i%2==0 else c.lower() for i,c in enumerate(t))}")
    fonts.append(f"7. Spaced: {' '.join(t)}")
    fonts.append(f"8. Dot: {'.'.join(t)}")
    fonts.append(f"9. Line: {'_'.join(t)}")
    fonts.append(f"10. Wave: {''.join(f'{c}~' for c in t)}")
    fonts.append(f"11. Brackets: {''.join(f'[{c}]' for c in t)}")
    fonts.append(f"12. Small: {t.lower()}")
    fonts.append(f"13. Big: {t.upper()}")
    fonts.append(f"14. Mirror: {t} | {t[::-1]}")
    fonts.append(f"15. Double: {t+t}")
    fonts.append(f"16. Cute: ♡ {t} ♡")
    fonts.append(f"17. King: ♔ {t} ♔")
    fonts.append(f"18. Fire: 🔥 {t} 🔥")
    fonts.append(f"19. Star: ★ {t} ★")
    fonts.append(f"20. Length: {len(t)} chars")
    
    # Pro Unicode fonts (will show on mobile)
    try:
        bold_sans = ''.join(chr(0x1D5D4 + ord(c)-97) if 'a'<=c<='z' else chr(0x1D5D0 + ord(c.lower())-97) if 'A'<=c<='Z' else c for c in t)
        fonts.append(f"21. 𝗕𝗼𝗹𝗱 

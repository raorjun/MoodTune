from ytmusicapi import setup

# Generate authentication JSON file for YouTube Music
setup(
    filepath="backend/config/browser.json", 
    headers_raw="""POST /youtubei/v1/browse?ctoken=4qmFsgI0EiRWTFBMbW5oSW5adjNVYURIMzFZOW56Y0lUS29MelhxM2traFkaDGtnRURDT1VFOEFFQg%253D%253D&continuation=4qmFsgI0EiRWTFBMbW5oSW5adjNVYURIMzFZOW56Y0lUS29MelhxM2traFkaDGtnRURDT1VFOEFFQg%253D%253D&type=next&itct=CBgQybcCIhMIsYDWxeugigMVAYXkBh1c5Dsd&prettyPrint=false HTTP/2
Host: music.youtube.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:133.0) Gecko/20100101 Firefox/133.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Content-Type: application/json
Content-Length: 2741
Referer: https://music.youtube.com/browse/VLPLmnhInZv3UaDH31Y9nzcITKoLzXq3kkhY
X-Goog-Visitor-Id: Cgt4WHNwRExsNVE2ayixuOi6BjIKCgJVUxIEGgAgOg%3D%3D
X-Youtube-Bootstrap-Logged-In: true
X-Youtube-Client-Name: 67
X-Youtube-Client-Version: 1.20241209.01.00
X-Goog-AuthUser: 0
X-Origin: https://music.youtube.com
Origin: https://music.youtube.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: same-origin
Sec-Fetch-Site: same-origin
Authorization: SAPISIDHASH 1733958706_13ee4385d01fe67578cca977797c33c9f42947a8_u SAPISID1PHASH 1733958706_13ee4385d01fe67578cca977797c33c9f42947a8_u SAPISID3PHASH 1733958706_13ee4385d01fe67578cca977797c33c9f42947a8_u
Connection: keep-alive
Alt-Used: music.youtube.com
Cookie: YSC=pSU9WmIUPUo; VISITOR_INFO1_LIVE=xXspDLl5Q6k; VISITOR_PRIVACY_METADATA=CgJVUxIEGgAgOg%3D%3D; _gcl_au=1.1.1665712200.1733954211; __Secure-1PSIDTS=sidts-CjIB7wV3sahbXkln96LrYzS76S_kv1IpEGt5wcwiZh49X9Nrjb6xMmbcOTTb0fAwo-LDURAA; __Secure-3PSIDTS=sidts-CjIB7wV3sahbXkln96LrYzS76S_kv1IpEGt5wcwiZh49X9Nrjb6xMmbcOTTb0fAwo-LDURAA; HSID=ANNaLCt9ncHbD0wJv; SSID=A0SUjAVLoypgNvrPH; APISID=pC7E6wQ9Hp4ANXGQ/AyN6SJWTc9s-EzFm5; SAPISID=7K05vXM1nwT-oXXu/AgAR1qKjWC9IljuG-; __Secure-1PAPISID=7K05vXM1nwT-oXXu/AgAR1qKjWC9IljuG-; __Secure-3PAPISID=7K05vXM1nwT-oXXu/AgAR1qKjWC9IljuG-; SID=g.a000rAhp-U7zlIFnbd9ZTujwlacJkkeJinvjmYcFZbXKO-Z9EdRztBRv_Pm6-HQ4eEakbST3DAACgYKAQQSARUSFQHGX2MiW4EQfc-C55qL0L5e9X7xpRoVAUF8yKpPZm65dApWmadvh-gtMVjh0076; __Secure-1PSID=g.a000rAhp-U7zlIFnbd9ZTujwlacJkkeJinvjmYcFZbXKO-Z9EdRzDjGuBARh5fWSfoWzkeBZVAACgYKAfkSARUSFQHGX2MiqFY39BfU61Upmn3-yOtKGxoVAUF8yKomGm9AmZqYAuHJnwTsG7O10076; __Secure-3PSID=g.a000rAhp-U7zlIFnbd9ZTujwlacJkkeJinvjmYcFZbXKO-Z9EdRzDHpGwsXnfgsgaYgADZLVvwACgYKAUASARUSFQHGX2Mi78d4eBFCT9o7PHpA2cQ1sRoVAUF8yKqAkZcmT4QLa_jD1huYF5vQ0076; LOGIN_INFO=AFmmF2swRQIgMAtO07CH58M9dtVJ6qZxn8LPjJTQX76xI4vVwrrw2YsCIQDYQlNR5SdLSXoxQop0XPeQ6TnkTzQNzVgLATyxRKuEQg:QUQ3MjNmeEg2MFhwWmJHamU0TWFuc2YxQzExcWVEaXZLOEZqQ3pfcW8wcG53UU4wdmhJcFFtRDdmZjhDa2E0QVZlODhPRGU0Um92MHotY3l4YjdKU3pwYUhXUzZadWhvWE5oNF82eXk3YmRGMXB6NlpUbUJGeUdCX0hkLVh2cTJ4MjNHeUUtUnRhbzZWNDUxOU43MTkzdVF0UEg2OHhRVkh3; SIDCC=AKEyXzWclgP4TQOUp9euUttepem-NQRZ2ie0_SNL-jgHmjQaMNZS3KVhKiTT8OKpcXa2-KS6og; __Secure-1PSIDCC=AKEyXzWbkuHDuDnu39T4rHoSme-A7ukvYkBwG65safrx8v1-8TbVDspJ8mshjx_HsD0ZnDTGTA; __Secure-3PSIDCC=AKEyXzUFNkxH-otEVUfYH-nKYA9E-L_u1C2vfk5rcVTFYuLo2JqQrXJjOHYPEm_oPhTRRbg-
DNT: 1
Sec-GPC: 1
Priority: u=4
TE: trailers"""
)

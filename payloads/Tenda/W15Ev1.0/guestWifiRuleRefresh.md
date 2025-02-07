## Overview

- Firmware download website: https://www.tendacn.com/download/detail-2722.html

## Affected version

W15EV1.0 V15.11.0.14

## Vulnerability details

The Tenda W15EV1.0 V15.11.0.14 firmware has a stack overflow vulnerability in the `guestWifiRuleRefresh` function. The `gstUp, gstDwn` variable receives the `qosGuestUpstream, qosGuestDownstream` parameter from a POST request. However, since the user can control the input of `qosGuestUpstream, qosGuestDownstream`, the statement

```c
sprintf(
      (char *)gstRuleQos,
      "%d;1;gst;%s;%s;%s;0;0;0;1",
      gstIdQos,
      (const char *)gstIpRng,
      (const char *)gstUp,
      (const char *)gstDwn);
```

can cause a buffer overflow. The user-provided `qosGuestUpstream, qosGuestDownstream` can exceed the capacity of the `gstRuleQos` array, triggering this security vulnerability.

![image-20240417111636433](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417111636433.png)

![image-20240417111650219](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240417111650219.png)

## POC

![image-20240416114043980](https://raw.githubusercontent.com/abcdefg-png/images2/main/image-20240416114043980.png)

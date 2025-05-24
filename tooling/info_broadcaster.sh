#!/bin/bash
# Collect basic system information and save to system_info.txt

output_file="system_info.txt"
> "$output_file"

echo "==================== SYSTEM INFORMATION ====================" >> "$output_file"
echo "Generated on: $(date)" >> "$output_file"
echo "------------------------------------------------------------" >> "$output_file"

echo "[*] Getting Broadcast Information..."
broadcast_info=$(ifconfig | grep broadcast)
echo -e "Broadcast Info:\n$broadcast_info" | tee -a "$output_file"

echo "[*] Getting IP Information..."
inet_info=$(ifconfig | grep inet)
echo -e "IP Info:\n$inet_info" | tee -a "$output_file"

echo "[*] Getting MAC Address Information..."
mac_info=$(ifconfig | grep ether)
echo -e "MAC Info:\n$mac_info" | tee -a "$output_file"

echo "[*] Getting Radio Interface Name..."
radio_name=$(iw dev 2>/dev/null | awk '$1=="Interface"{print $2}')
echo -e "Radio Interface: $radio_name" | tee -a "$output_file"

echo "[*] Listing USB Devices..."
usb_info=$(lsusb)
echo -e "USB Info:\n$usb_info" | tee -a "$output_file"

echo "System information has been saved to '$output_file'."

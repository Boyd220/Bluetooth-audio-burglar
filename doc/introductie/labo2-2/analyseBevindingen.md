# XPhost
Ipadres: 192.168.55.91

OS: Windows XP (Windows 2000 LAN Manager)

PORT     STATE  SERVICE       VERSION
139/tcp  open   netbios-ssn   Microsoft Windows 98 netbios-ssn
445/tcp  open   microsoft-ds  Microsoft Windows XP microsoft-ds
2869/tcp closed icslap
3389/tcp open   ms-wbt-server Microsoft Terminal Service
Service Info: OSs: Windows 98, Windows XP, Windows; CPE: cpe:/o:microsoft:windows_98, cpe:/o:microsoft:windows_xp, cpe:/o:microsoft:windows

#Jeroen's PC
Ipadres: 192.168.55.1

OS: Too many fingerprints match this host to give specific OS details

Er staan geen poorten open

#Boyd's PC
Ipadres: 172.16.235.189

OS: OS: Windows 10 Home 14393 (Windows 10 Home 6.3)

PORT    STATE SERVICE         VERSION
135/tcp open  msrpc           Microsoft Windows RPC
139/tcp open  netbios-ssn     Microsoft Windows 98 netbios-ssn
445/tcp open  microsoft-ds    Microsoft Windows 7 or 10 microsoft-ds
902/tcp open  ssl/vmware-auth VMware Authentication Daemon 1.10 (Uses VNC, SOAP)
912/tcp open  vmware-auth     VMware Authentication Daemon 1.0 (Uses VNC, SOAP)

#Bekijk hoe nmap en de vulnrability scanners andere resultaten geven wanneer je je firewall aan/afzet
Er is geen verschil met de resultaten bij het aan en uit zetten van de firewall Services aan en uitschakelen heeft wel effect, zo kunnen we ssh aanzetten en dan wordt deze ook gedetecteerd

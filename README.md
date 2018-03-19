# External IP Address Checker

Are you looking for a way to periodically check the external IP address of the router in your home provided by your ISP, however, you don't want to pay for this service? Well, look no further! The External IP Address Checker will keep you updated and connected through your VPN even if the IP Address changes while you're on the road!

Prerequisites:
- OpenVPN installed and configured
- Install the listed modules from the import statements
- SMTP information (Outlook is included as the default)

The python program will check the IP address (default is every 5 hours) of your external router then will update the configuration file used for OpenVPN with the updated IP Address, create the new Client OVPN file, and then send the updated IP Address and OVPN via email. All of the settings are saved in the accompanying configuration file.

The IP Address is checked against free URLs. The code is using a default service, however, the source code file has a starting list to choose from.

Future updates will include encrypting the configuration file and moving some of the functionality to a class.


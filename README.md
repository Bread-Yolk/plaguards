# Plaguards: Open Source PowerShell Deobfuscation and IOC Detection Engine for Blue Teams.

![Plaguards](https://github.com/user-attachments/assets/f902d2b5-43ec-4919-b880-d41a64db2f15)

[![License](https://img.shields.io/badge/License-AGPLv3-purple.svg?&logo=none)](https://www.gnu.org/licenses/agpl-3.0)
![Powershell-Deobfuscator](https://img.shields.io/badge/powershell_deobfuscator-blue)
![Powershell-Deobfuscator](https://img.shields.io/badge/ioc_checker-red)

<p align="justify">Plaguards is a cutting-edge security tool built to streamline and automate the deobfuscation of obfuscated PowerShell scripts, empowering security teams to rapidly identify Indicators of Compromise (IOCs) and determine whether they represent verified threats (VT) or false positives (FP). Each analysis is documented in a comprehensive PDF report, designed to provide deep insights and actionable intelligence.

As a web app, Plaguards offers users the flexibility to conduct powerful, on-demand analysis from anywhere, at any time, making it invaluable to blue teams tasked with responding to complex malware threats. This innovation not only accelerates workflows but also enhances detection accuracy, positioning Plaguards as a vital asset in proactive threat response.</p>


## Security Warning

WARNING: There are known security vulnerabilities within certain versions of Plaguards. Before proceeding, please read through Plaguards [Security Advisories]() for a better understanding of how you might be impacted.

## Main Features

|No.|Main Features|Notes|
|:-:|:------------:|:---:|
|1. | IOC Checker.|Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed purus nulla, congue vel tincidunt lobortis, tincidunt eget nisi. Sed iaculis suscipit tortor id laoreet. Duis et ipsum nec dolor iaculis aliquet. Integer ultricies urna nec tristique vehicula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce lacinia ex non facilisis pellentesque. Cras vitae magna porttitor, rutrum ipsum quis, tristique dolor. Sed porttitor convallis sapien, non dictum leo fringilla eget. |
|2. | Powershell Deobfuscation.|Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed purus nulla, congue vel tincidunt lobortis, tincidunt eget nisi. Sed iaculis suscipit tortor id laoreet. Duis et ipsum nec dolor iaculis aliquet. Integer ultricies urna nec tristique vehicula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce lacinia ex non facilisis pellentesque. Cras vitae magna porttitor, rutrum ipsum quis, tristique dolor. Sed porttitor convallis sapien, non dictum leo fringilla eget. |
|3. | Automated Reporting in PDF format.|Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed purus nulla, congue vel tincidunt lobortis, tincidunt eget nisi. Sed iaculis suscipit tortor id laoreet. Duis et ipsum nec dolor iaculis aliquet. Integer ultricies urna nec tristique vehicula. Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Fusce lacinia ex non facilisis pellentesque. Cras vitae magna porttitor, rutrum ipsum quis, tristique dolor. Sed porttitor convallis sapien, non dictum leo fringilla eget. |

## Requirements

- VPN Server (Recommended for Production Server).
- Domain for HTTPS (Recommended for Production Server).
- Docker
- Docker Compose v2
- Python 3.x
- Port 8000

**(No manual installation needed – we’ll handle everything for you!)**

## Deployment and Usage

#### To deploy Plaguards:

1. Clone this repository.

> Command

```txt
git clone https://github.com/Bread-Yolk/plaguards.git
cd plaguards-main
```

2. Run the setup script.

```txt
./plaguards.sh
```

3. By default, Plaguards dashboard will listen at port **8000**.


## Demo


## Authors
- [jon-brandy](https://github.com/jon-brandy)
- [LawsonSchwantz](https://github.com/LawsonSchwantz)
- [tkxldk](https://github.com/tkxldk)

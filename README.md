# FrostNet 🔍
### Network Scanner & Security Analyzer

A lightweight **Python-based network security tool** with CLI and Web Dashboard interfaces for scanning open ports, identifying services, and evaluating basic security exposure.

![Python](https://img.shields.io/badge/Python-3.10+-f8c8dc?style=for-the-badge&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-Web%20App-fde68a?style=for-the-badge&logo=flask&logoColor=white)
![Status](https://img.shields.io/badge/Status-Active-fbcfe8?style=for-the-badge)

---

## ☁️ Overview 

**NetScope** is a simple network security tool :

It provides:
- Port scanning (TCP)
- Basic service detection
- Security score evaluation
- Scan history tracking
- Web dashboard interface

---

## Interfaces

### CLI Mode

```bash
python scan.py
```

## 🌐 Web Dashboard
```bash
python app.py
```
**Then open:**
```bash
http://127.0.0.1:5000
```

## 📄 Features

* Multi-threaded port scanning
* Service identification (HTTP, SSH, FTP, etc.)
* Web interface (Flask)
* Scan history storage
* Security score system

## 📁 Output Files

* report.txt → CLI scan results
* history.json → scan history
* report.json → latest scan data

## Example Output

80 - HTTP  
443 - HTTPS  
135 - RPC  

Security Score: 85/100

## 🧸 Disclaimer

This project is for educational purposes only.
Do not use it on systems without authorization.

## 🤍 Author

Cybersecurity learning project focused on:

* Networking fundamentals
* Python development
* Web applications (Flask)
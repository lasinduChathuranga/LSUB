# LSUB v1 - Enhanced Subdomain Enumeration Tool
LSUB v1 is a powerful subdomain enumeration tool designed for cybersecurity professionals. It integrates 12 different engines including search engines and specialized data sources like SSL certificate logs. With features like multi-threading, bruteforce support, port scanning, and customizable output formats, LSUB helps in comprehensive discovery of subdomains for vulnerability assessments and penetration testing.

## 🚀 Features

### Search Engines Integration (6 Engines)
- **Google** - Web search enumeration
- **Bing** - Microsoft search engine
- **Yahoo** - Yahoo search integration
- **Baidu** - Chinese search engine
- **Ask** - Ask.com search
- **Netcraft** - Domain intelligence

### Specialized Engines (6 Engines)
- **SSL Certificates (crt.sh)** - Enhanced certificate transparency logs
- **DNSdumpster** - DNS reconnaissance
- **VirusTotal** - Threat intelligence platform
- **ThreatCrowd** - Open source threat intelligence
- **PassiveDNS** - Passive DNS data
- **Certificate Transparency** - Alternative SSL cert lookup

### Advanced Features
- 🎯 **Multi-threaded scanning** for faster results
- 🔍 **Bruteforce capability** with customizable wordlists
- 🌐 **12 different enumeration engines**
- 📊 **Port scanning** on discovered subdomains
- 💾 **Multiple output formats**
- 🎨 **Colorized terminal output**
- ⚡ **Enhanced crt.sh integration** with JSON and HTML parsing
- 🔧 **Flexible engine selection**

## 📦 Installation

### Prerequisites
```bash
# Python 2.7 or 3.x
python --version

# Install required dependencies
pip install -r requirements.txt
```

### Clone Repository
```bash
git clone https://github.com/lasinduChathuranga/LSUB.git
cd LSUB
python3 lsub-v1.py -d example.com
```

## 🛠️ Dependencies

```
requests>=2.25.1
dnspython>=2.1.0
```

Optional dependencies for enhanced functionality:
```
subbrute  # For bruteforce functionality
```

## 📋 Usage

### Basic Usage
```bash
# Simple subdomain enumeration
python lsub-v1.py -d example.com

# With verbose output
python lsub-v1.py -d example.com -v

# Save results to file
python lsub-v1.py -d example.com -o results.txt
```

### Advanced Usage
```bash
# Use specific engines only
python lsub-v1.py -d example.com -e google,ssl,dnsdumpster

# Enable bruteforce with custom threads
python lsub-v1.py -d example.com -b -t 50

# Include port scanning
python lsub-v1.py -d example.com -p 80,443,8080,8443

# Use only search engines
python lsub-v1.py -d example.com -e google,bing,yahoo,baidu,ask,netcraft

# Use only specialized engines
python lsub-v1.py -d example.com -e ssl,dnsdumpster,virustotal,threatcrowd,passivedns
```

### Show Available Engines
```bash
python lsub-v1.py --show-engines
```

## 🎛️ Command Line Options

| Option | Description | Example |
|--------|-------------|---------|
| `-d, --domain` | Target domain (required) | `-d example.com` |
| `-e, --engines` | Comma-separated list of engines | `-e google,ssl,bing` |
| `-t, --threads` | Number of threads (default: 30) | `-t 50` |
| `-b, --bruteforce` | Enable bruteforce enumeration | `-b` |
| `-p, --ports` | Scan ports on discovered subdomains | `-p 80,443,8080` |
| `-o, --output` | Output file for results | `-o results.txt` |
| `-v, --verbose` | Enable verbose output | `-v` |
| `--no-color` | Disable colored output | `--no-color` |
| `--show-engines` | Display available engines | `--show-engines` |

## 🏗️ Engine Categories

### Search Engines Group
Perfect for discovering subdomains indexed by search engines:
- Google, Bing, Yahoo, Baidu, Ask, Netcraft

### Specialized Engines Group  
Advanced discovery through specialized databases:
- SSL Certificate databases, DNS databases, Threat intelligence platforms

## 📈 Performance Tips

1. **Adjust thread count** based on your system and network:
   ```bash
   python lsub-v1.py -d example.com -t 100  # High-performance systems
   python lsub-v1.py -d example.com -t 20   # Conservative approach
   ```

2. **Use specific engines** for targeted discovery:
   ```bash
   python lsub-v1.py -d example.com -e ssl,dnsdumpster  # Focus on cert transparency
   ```

3. **Combine with bruteforce** for comprehensive coverage:
   ```bash
   python lsub-v1.py -d example.com -b -t 50
   ```

## 📊 Output Examples

### Console Output
```
╔══════════════════════════════════════════════════════════════════════╗
║                           TARGET ANALYSIS                            ║
╠══════════════════════════════════════════════════════════════════════╣
║ Enumerating subdomains for: example.com                              ║
╚══════════════════════════════════════════════════════════════════════╝

[+] Using 12 enumeration engines
    Search Engines: 6/6
    Specialized Engines: 6/6

╔══════════════════════════════════════════════════════════════════════╗
║ Searching  now  SSL Certificates (crt.sh)                            ║
╚══════════════════════════════════════════════════════════════════════╝

[+] www.example.com
[+] mail.example.com
[+] ftp.example.com
[+] api.example.com

[+] Found 45 subdomains
[+] Scan completed in 23.45 seconds
```

### File Output
```
# LSUB v1 Enhanced Results
# Generated: 2025-06-15 14:30:22
# Total: 45

api.example.com
ftp.example.com
mail.example.com
www.example.com
...
```

## 🔧 Configuration

### Custom Wordlists (for bruteforce)
Place your custom wordlist in the `subbrute/` directory:
```
subbrute/
├── names.txt        # Default wordlist
├── resolvers.txt    # DNS resolvers
└── custom.txt       # Your custom wordlist
```

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Areas for Contribution
- Additional enumeration engines
- Performance optimizations
- New output formats
- Documentation improvements
- Bug fixes and testing

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is intended for educational purposes and authorized penetration testing only. Users are responsible for complying with applicable laws and regulations. The developers assume no liability for misuse of this tool.

## 🐛 Bug Reports & Feature Requests

- **Bug Reports**: [GitHub Issues](https://github.com/yourusername/lsub-v1/issues)
- **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/lsub-v1/discussions)

## 📚 Documentation

For detailed documentation and advanced usage examples, visit our [Wiki](https://github.com/yourusername/lsub-v1/wiki).

## 🙏 Acknowledgments

- Thanks to the certificate transparency community
- Special thanks to crt.sh for SSL certificate data
- Inspired by various subdomain enumeration tools in the security community

## 📊 Statistics

- **12 enumeration engines**
- **Multi-threaded performance**
- **Enhanced SSL certificate integration**
- **Cross-platform compatibility**

---

**Made with ❤️ for the cybersecurity community**



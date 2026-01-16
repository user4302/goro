# Security Policy

## 🛡️ Security Reporting

We take the security of Goro seriously. If you discover a security vulnerability, please report it responsibly.

### How to Report

**Important:** For security concerns, please open an issue on GitLab: https://gitlab.com/user4302_Projects/coding/python/textual/goro/-/issues

When reporting a security issue, please include:
- **Vulnerability description** and potential impact
- **Steps to reproduce** the issue (if applicable)
- **Affected versions** of Goro
- **Proposed mitigation** (if known)

### Response Time

We aim to respond to security reports within:
- **48 hours** for critical vulnerabilities
- **72 hours** for high severity issues
- **1 week** for medium and low severity issues

### Supported Versions

Security updates are provided for:
- **Current stable version** (v0.5.x)
- **Previous minor version** (v0.4.x) for 6 months after new release

Older versions may not receive security updates.

## 🔒 Security Considerations

### Git Operations

Goro executes Git commands on your local system. To maintain security:

- **Repository paths** are validated before operations
- **Command injection** is prevented through proper argument escaping
- **User permissions** are respected - Goro only operates with your current user privileges

### Configuration Files

- Configuration is stored in `~/.goro/config.yaml`
- File permissions are set to user-read/write only
- No sensitive data (passwords, tokens) is stored in configuration

### Network Access

- Goro only accesses local Git repositories
- No network requests are made except for Git operations
- No telemetry or data collection is performed

## 🚨 Common Security Issues

### Path Traversal

Goro validates all repository paths to prevent path traversal attacks. Only paths within the user's accessible file system are allowed.

### Command Injection

All Git commands are executed with proper argument escaping to prevent command injection attacks.

### Privilege Escalation

Goro does not attempt to elevate privileges and operates with the current user's permissions only.

## 📋 Security Best Practices for Users

1. **Keep Goro updated** to the latest version
2. **Review repository paths** before adding them to Goro
3. **Use secure Git credentials** (SSH keys, credential helpers)
4. **Regularly review** the repositories managed by Goro
5. **Backup configuration** before major changes

## 🔐 Third-Party Dependencies

Goro uses the following main dependencies:
- **Textual** - TUI framework
- **Typer** - CLI framework  
- **Pydantic** - Data validation
- **Rich** - Terminal formatting

We monitor these dependencies for security updates and update them promptly.

## 📞 Security Contact

For security-related issues that require confidential communication, please open an issue on GitLab with the "Security" label: https://gitlab.com/user4302_Projects/coding/python/textual/goro/-/issues

**Note:** We do not provide email or direct messaging support for security issues. All security communication should go through GitLab Issues.

## 🏆 Security Acknowledgments

We thank security researchers and users who help keep Goro secure by reporting vulnerabilities responsibly.

---

*This security policy is part of Goro's commitment to maintaining a secure and trustworthy tool for the developer community.*

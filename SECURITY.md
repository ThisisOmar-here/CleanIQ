# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.x.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of CleanIQ seriously. If you believe you have found a security vulnerability, please report it to us as described below.

**Please do not report security vulnerabilities through public GitHub issues.**

### How to Report

1. **Email**: Send a detailed report to the project maintainer
2. **Include**:
   - Type of issue (e.g., path traversal, arbitrary file access, etc.)
   - Full paths of source file(s) related to the issue
   - Step-by-step instructions to reproduce the issue
   - Proof-of-concept or exploit code (if possible)
   - Impact of the issue

### What to Expect

- **Acknowledgment**: We will acknowledge your report within 48 hours
- **Updates**: We will keep you informed about our progress
- **Resolution**: We aim to resolve critical issues within 7 days
- **Credit**: We will credit you in our release notes (unless you prefer to remain anonymous)

## Security Considerations

CleanIQ is designed with privacy in mind:

- **100% Local Processing**: All file analysis happens on your machine
- **No Cloud Upload**: Your files are never sent to external servers
- **Ollama Integration**: AI processing uses your local Ollama installation
- **Safe Deletion**: By default, files are moved to Recycle Bin, not permanently deleted

### File Access

CleanIQ requires read access to scan directories and write access to delete files. The application:

- Only accesses paths explicitly requested by the user
- Excludes system-critical directories by default
- Does not store or transmit file contents

## Best Practices for Users

1. Review files before deletion
2. Use the "Safe to Delete" indicator as a guide, not absolute truth
3. Keep backups of important data
4. Run the application with standard user privileges (not admin)

---

Thank you for helping keep CleanIQ and our users safe!

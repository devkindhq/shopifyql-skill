# Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.5.x   | :white_check_mark: |
| < 1.5   | :x:                |

## Reporting a Vulnerability

If you discover a security vulnerability, please report it responsibly:

- **Email**: ali@devkind.com.au
- **Do not** open a public GitHub issue for security vulnerabilities
- **Response time**: You will receive a response within 48 hours

Please include as much detail as possible:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Any suggested fixes (optional)

## Credential Safety

This project is designed with security in mind:

- Shopify API tokens **never** pass through Claude context
- The script reads credentials from environment variables only
- No credentials are logged or stored in memory beyond their immediate use

If you believe you have found a way that credentials could be exposed, please report it immediately using the process above.

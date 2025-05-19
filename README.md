# Exasol TLS Challenge

This project is a solution to the Exasol TLS Programming Challenge. It involves:
- Connecting securely to a TLS server using provided certificates
- Solving a proof-of-work challenge
- Responding to identity prompts interactively

## 🛠 Requirements

- Python 3.8+
- `client.crt`, `client.key`, and `ca.crt` (provided by challenge admin)

## 🚀 How to Run

Clone the repo and place the certificate files in the root directory:

```bash
python3 exasol_challenge.py

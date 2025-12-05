# Email List Validator & Formatter

A professional Python toolkit to clean, verify, and format email lists for marketing platforms (e.g., MailPoet, MailChimp).

## 🚀 Features

* **Clean:** Removes duplicate lines instantly.
* **Verify:** Checks syntax and performs real-time DNS MX record lookups to ensure the domain exists. Uses Multi-threading for high speed.
* **Generate:** Converts raw text lists into CSVs with "First Name" and "Last Name" auto-extracted from email addresses.

## 📖 Usage

### 1. Cleanup Duplicates
Takes a text file and removes duplicates.

```bash 
	python3 clean.py list.txt
	# Output: list_clean.txt
```

## 2. Verify Emails (DNS Check)
Checks if the email is deliverable.
```bash
	python3 verify.py list_clean.txt
	# Output: verified_valid.txt, verified_invalid.txt
```
## 3. Generate CSV
Prepares the file for import into email marketing tools.
```bash
	python3 generate.py verified_valid.txt
	# Output: verified_valid_import.csv
```

## ⚖ License
MIT



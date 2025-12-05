#!/usr/bin/env python3
import argparse
import os
import sys
import concurrent.futures
from email_validator import validate_email, EmailNotValidError

class EmailVerifier:
    def __init__(self, input_file, workers=10):
        self.input_file = input_file
        self.valid_file = "verified_valid.txt"
        self.invalid_file = "verified_invalid.txt"
        self.workers = workers

    def verify_single_email(self, email):
        """Checks a single email and returns tuple (email, is_valid, reason)"""
        try:
            # check_deliverability=True performs the DNS check
            validate_email(email, check_deliverability=True)
            return (email, True, "Valid")
        except EmailNotValidError as e:
            return (email, False, str(e))

    def process(self):
        if not os.path.exists(self.input_file):
            print(f"Error: File '{self.input_file}' not found.")
            sys.exit(1)

        print(f"Loading emails from {self.input_file}...")
        with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as f:
            emails = [line.strip() for line in f if line.strip()]

        print(f"Starting verification for {len(emails)} emails using {self.workers} threads...")
        
        valid_list = []
        invalid_list = []

        # ThreadPoolExecutor runs checks in parallel
        with concurrent.futures.ThreadPoolExecutor(max_workers=self.workers) as executor:
            results = executor.map(self.verify_single_email, emails)
            
            for i, result in enumerate(results):
                email, is_valid, reason = result
                if is_valid:
                    valid_list.append(email)
                else:
                    invalid_list.append(f"{email} | Reason: {reason}")
                
                # Simple progress indicator
                if (i + 1) % 50 == 0:
                    print(f"Processed {i + 1}/{len(emails)}...")

        self._save_results(valid_list, invalid_list)

    def _save_results(self, valid, invalid):
        with open(self.valid_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(valid) + '\n')
            
        with open(self.invalid_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(invalid) + '\n')

        print("\n--- Verification Complete ---")
        print(f"✔ Valid: {len(valid)} (Saved to {self.valid_file})")
        print(f"✖ Invalid: {len(invalid)} (Saved to {self.invalid_file})")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Verify email validity and DNS records.")
    parser.add_argument("file", help="Path to the input text file")
    parser.add_argument("--workers", type=int, default=10, help="Number of parallel threads (default: 10)")
    args = parser.parse_args()

    verifier = EmailVerifier(args.file, args.workers)
    verifier.process()

#!/usr/bin/env python3
import argparse
import os
import csv
import sys

class CSVGenerator:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = self._generate_output_name()

    def _generate_output_name(self):
        base, _ = os.path.splitext(self.input_file)
        return f"{base}_import.csv"

    def _clean_name(self, name_part):
        """Cleans name strings by removing numbers and special chars."""
        # Replace common separators with space
        cleaned = name_part.replace('.', ' ').replace('_', ' ').replace('-', ' ')
        # Remove digits if strictly name extraction is desired (optional)
        cleaned = ''.join([i for i in cleaned if not i.isdigit()])
        return cleaned.title().strip()

    def _parse_email_to_name(self, email):
        local_part = email.split('@')[0]
        
        # Heuristic: Firstname.Lastname
        if '.' in local_part:
            parts = local_part.split('.')
            first = self._clean_name(parts[0])
            last = self._clean_name(' '.join(parts[1:]))
            return first, last
        
        # Heuristic: Firstname_Lastname
        elif '_' in local_part:
            parts = local_part.split('_')
            first = self._clean_name(parts[0])
            last = self._clean_name(' '.join(parts[1:]))
            return first, last

        # Fallback: Treat whole local part as First Name
        else:
            return self._clean_name(local_part), ""

    def process(self):
        if not os.path.exists(self.input_file):
            print(f"Error: File '{self.input_file}' not found.")
            sys.exit(1)

        print(f"Converting {self.input_file} to CSV...")

        try:
            with open(self.input_file, 'r', encoding='utf-8') as f_in, \
                 open(self.output_file, 'w', newline='', encoding='utf-8') as f_out:
                
                # MailPoet standard headers
                fieldnames = ['Email', 'First Name', 'Last Name']
                writer = csv.DictWriter(f_out, fieldnames=fieldnames)
                writer.writeheader()

                lines = f_in.read().splitlines()
                count = 0

                for email in lines:
                    email = email.strip().lower()
                    if not email:
                        continue

                    first, last = self._parse_email_to_name(email)
                    
                    writer.writerow({
                        'Email': email,
                        'First Name': first,
                        'Last Name': last
                    })
                    count += 1

            print(f"✔ Success! Converted {count} contacts.")
            print(f"✔ Ready for MailPoet: {self.output_file}")

        except Exception as e:
            print(f"Error during conversion: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert email list to MailPoet-ready CSV.")
    parser.add_argument("file", help="Path to the input text file")
    args = parser.parse_args()

    generator = CSVGenerator(args.file)
    generator.process()

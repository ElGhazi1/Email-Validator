#!/usr/bin/env python3
import argparse
import os
import sys

class EmailCleaner:
    def __init__(self, input_file):
        self.input_file = input_file
        self.output_file = self._generate_output_name()

    def _generate_output_name(self):
        base, ext = os.path.splitext(self.input_file)
        return f"{base}_clean{ext}"

    def process(self):
        if not os.path.exists(self.input_file):
            print(f"Error: File '{self.input_file}' not found.")
            sys.exit(1)

        print(f"Reading {self.input_file}...")
        
        try:
            with open(self.input_file, 'r', encoding='utf-8', errors='ignore') as f:
                # Use a set to automatically remove duplicates
                raw_lines = f.read().splitlines()
                
            unique_emails = set(line.strip() for line in raw_lines if line.strip())
            
            # Sort them for neatness
            sorted_emails = sorted(unique_emails)

            with open(self.output_file, 'w', encoding='utf-8') as f:
                f.write('\n'.join(sorted_emails))
                f.write('\n')

            print(f"✔ Success! Removed {len(raw_lines) - len(sorted_emails)} duplicates.")
            print(f"✔ Clean list saved to: {self.output_file}")
            
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Clean and remove duplicate emails from a text file.")
    parser.add_argument("file", help="Path to the input text file")
    args = parser.parse_args()

    cleaner = EmailCleaner(args.file)
    cleaner.process()

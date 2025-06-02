#!/usr/bin/env python3
import argparse

from worker.tasks.pdf_extract import extract_tables


def main():
    parser = argparse.ArgumentParser(description="Run extract_tables task synchronously")
    parser.add_argument("job_id")
    parser.add_argument("s3_key")
    args = parser.parse_args()

    output_key = extract_tables(args.job_id, args.s3_key)
    print(f"Output stored at: {output_key}")


if __name__ == "__main__":
    main()

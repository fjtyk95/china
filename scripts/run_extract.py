import sys
from worker.tasks.pdf_extract import extract_tables
from worker.database import Base, engine

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print('Usage: python scripts/run_extract.py <job_id> <s3_key>')
        sys.exit(1)

    job_id = sys.argv[1]
    s3_key = sys.argv[2]

    # ensure tables exist
    Base.metadata.create_all(bind=engine)

    result = extract_tables.apply(args=(job_id, s3_key)).get()
    print(result)

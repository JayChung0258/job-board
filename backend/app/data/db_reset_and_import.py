import json
import os
import random
import string
import subprocess
import sys
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import settings
from app.core.db import Base
from app.models.job import Job
from app.models.job_tag import JobTag
from app.models.tag import Tag, TagCategory
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

# Database connection
engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Add the project root to Python path
backend_dir = str(Path(__file__).parent.parent.parent)
sys.path.append(backend_dir)

# Command execution utility


def run_command(command):
    """Run a shell command and print output"""
    print(f"Running: {command}")
    process = subprocess.run(command, shell=True, text=True, capture_output=True)
    if process.stdout:
        print(process.stdout)
    if process.stderr:
        print(process.stderr)
    return process.returncode == 0


# MOCK DATA GENERATION FUNCTIONS
def load_tags():
    """Load tags from tags.json"""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    tags_path = os.path.join(script_dir, "tags.json")

    with open(tags_path, "r") as f:
        tags_data = json.load(f)["tags"]

    return tags_data


def generate_job_id():
    """Generate a random job ID"""
    return "".join(random.choices(string.digits, k=10))


def generate_company_name():
    """Generate a random company name"""
    prefixes = [
        "Tech",
        "Data",
        "Cloud",
        "Digital",
        "Cyber",
        "AI",
        "Web",
        "App",
        "Code",
        "Dev",
    ]
    suffixes = [
        "Solutions",
        "Technologies",
        "Innovations",
        "Systems",
        "Labs",
        "Works",
        "Studio",
        "Group",
        "Team",
        "Inc",
    ]
    return f"{random.choice(prefixes)} {random.choice(suffixes)}"


def generate_job_position():
    """Generate a random job position"""
    prefixes = ["Senior", "Lead", "Principal", "Staff", "Junior", "Associate", "Chief"]
    positions = [
        "Engineer",
        "Developer",
        "Analyst",
        "Designer",
        "Architect",
        "Consultant",
        "Manager",
        "Specialist",
    ]
    domains = [
        "Software",
        "Web",
        "Data",
        "Cloud",
        "UI/UX",
        "DevOps",
        "Frontend",
        "Backend",
        "Full Stack",
        "Product",
    ]

    if random.random() < 0.7:
        return f"{random.choice(prefixes)} {random.choice(domains)} {random.choice(positions)}"
    else:
        return f"{random.choice(domains)} {random.choice(positions)}"


def generate_posting_date():
    """Generate a random posting date within the last 60 days"""
    today = datetime.now().date()
    days_ago = random.randint(1, 60)
    posting_date = today - timedelta(days=days_ago)
    return posting_date.strftime("%Y-%m-%d")


def generate_location():
    """Generate a random job location"""
    cities = [
        "San Francisco, CA",
        "New York, NY",
        "Austin, TX",
        "Seattle, WA",
        "Boston, MA",
        "Chicago, IL",
        "Denver, CO",
        "Los Angeles, CA",
        "Atlanta, GA",
        "Remote",
    ]
    return random.choice(cities)


def select_random_tags(tags_data):
    """Select random tags from each category, ensuring they make sense together"""
    selected_tags = {}

    # First, select a role
    selected_tags["role"] = [random.choice(tags_data["role"])]

    # Based on the role, select appropriate technology tags
    if "Frontend" in selected_tags["role"][0] or "UI" in selected_tags["role"][0]:
        tech_candidates = ["JavaScript", "TypeScript", "React"]
    elif (
        "Backend" in selected_tags["role"][0]
        or "Full-Stack" in selected_tags["role"][0]
    ):
        tech_candidates = ["Python", "Node.js", "FastAPI", "SQLAlchemy"]
    elif "DevOps" in selected_tags["role"][0]:
        tech_candidates = ["AWS", "Kubernetes", "Docker"]
    elif "Data" in selected_tags["role"][0]:
        tech_candidates = ["Python"]
    else:
        tech_candidates = tags_data["technology"]

    # Only include technologies that are in our tags.json
    available_techs = [t for t in tech_candidates if t in tags_data["technology"]]
    if available_techs:
        num_techs = min(random.randint(1, 3), len(available_techs))
        selected_tags["technology"] = random.sample(available_techs, num_techs)

    # Select skill tags based on role
    if "Frontend" in selected_tags["role"][0] or "UI" in selected_tags["role"][0]:
        skill_candidates = ["UI-Development", "Web-Development", "User-Experience"]
    elif "Backend" in selected_tags["role"][0]:
        skill_candidates = ["API-Development", "Database", "Microservices"]
    elif "DevOps" in selected_tags["role"][0]:
        skill_candidates = ["CI-CD", "Infrastructure", "Cloud-Computing"]
    elif "Data" in selected_tags["role"][0]:
        skill_candidates = ["Analytics", "Big-Data", "Machine-Learning", "AI"]
    elif "Business" in selected_tags["role"][0]:
        skill_candidates = ["Analytics", "User-Experience"]
    else:
        skill_candidates = tags_data["skill"]

    # Only include skills that are in our tags.json
    available_skills = [s for s in skill_candidates if s in tags_data["skill"]]
    if available_skills:
        num_skills = min(random.randint(1, 4), len(available_skills))
        selected_tags["skill"] = random.sample(available_skills, num_skills)

    # Select methodology tags if applicable
    if random.random() < 0.7:  # 70% chance to have methodology tags
        num_methods = random.randint(1, 3)
        selected_tags["methodology"] = random.sample(
            tags_data["methodology"], min(num_methods, len(tags_data["methodology"]))
        )

    # Select tool tags if applicable
    if random.random() < 0.6:  # 60% chance to have tool tags
        num_tools = random.randint(1, 2)
        selected_tags["tool"] = random.sample(
            tags_data["tool"], min(num_tools, len(tags_data["tool"]))
        )

    return selected_tags


def generate_mock_jobs(num_jobs=500):
    """Generate mock job data"""
    tags_data = load_tags()
    jobs = []

    for i in range(num_jobs):
        job_id = generate_job_id()
        company_name = generate_company_name()

        job = {
            "job_position": generate_job_position(),
            "job_link": f"https://example.com/jobs/{uuid.uuid4().hex[:10]}",
            "job_id": job_id,
            "company_name": company_name,
            "company_profile": f"https://example.com/companies/{uuid.uuid4().hex[:10]}",
            "job_location": generate_location(),
            "job_posting_date": generate_posting_date(),
            "tags": select_random_tags(tags_data),
        }

        jobs.append(job)

    return jobs


def save_mock_jobs(jobs):
    """Save mock jobs to mock_jobs.json"""
    output = {"jobs": jobs}

    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "mock_jobs.json")

    with open(output_path, "w") as f:
        json.dump(output, f, indent=2)

    print(f"Generated {len(jobs)} mock jobs and saved to {output_path}")


# DATABASE RESET FUNCTIONS
def extract_db_connection_details():
    """Extract database connection details from DATABASE_URL"""
    db_url = settings.DATABASE_URL
    db_parts = db_url.replace("postgresql://", "").split("/")
    connection_str = db_parts[0]
    db_name = db_parts[1].split("?")[0]  # Remove any query parameters

    if "@" in connection_str:
        auth, host_port = connection_str.split("@")
        user, password = auth.split(":")
        host = host_port.split(":")[0]
    else:
        host = connection_str.split(":")[0]
        user = os.environ.get("POSTGRES_USER", "postgres")
        password = os.environ.get("POSTGRES_PASSWORD", "postgres")

    return {"user": user, "password": password, "host": host, "db_name": db_name}


def disconnect_users(conn_details):
    """Disconnect all users from the database"""
    print(f"Disconnecting users from database {conn_details['db_name']}...")
    psql_conn = f"PGPASSWORD={conn_details['password']} psql -U {conn_details['user']} -h {conn_details['host']}"

    disconnect_query = f"""
    SELECT pg_terminate_backend(pg_stat_activity.pid)
    FROM pg_stat_activity
    WHERE pg_stat_activity.datname = '{conn_details['db_name']}'
    AND pid <> pg_backend_pid();
    """
    run_command(f'{psql_conn} -c "{disconnect_query}"')

    # Wait a moment for connections to close
    time.sleep(2)


def reset_database(conn_details):
    """Drop and recreate the database"""
    psql_conn = f"PGPASSWORD={conn_details['password']} psql -U {conn_details['user']} -h {conn_details['host']}"

    print(f"Dropping database {conn_details['db_name']}...")
    run_command(f"{psql_conn} -c 'DROP DATABASE IF EXISTS {conn_details['db_name']}'")

    print(f"Creating database {conn_details['db_name']}...")
    run_command(f"{psql_conn} -c 'CREATE DATABASE {conn_details['db_name']}'")


def run_migrations():
    """Run database migrations using Alembic"""
    print("Running database migrations...")
    migration_result = run_command(f"cd {backend_dir} && alembic upgrade head")

    if not migration_result:
        print("Migration failed! Trying to create tables directly...")
        Base.metadata.create_all(bind=engine)
        print("Tables created directly via SQLAlchemy")
    else:
        print("Migrations completed successfully")


# DATA IMPORT FUNCTIONS
def clear_existing_data(db: Session):
    """Clear existing data from tables"""
    try:
        db.query(JobTag).delete()
        db.query(Job).delete()
        db.query(Tag).delete()
        db.commit()
        print("Cleared existing data")
    except Exception as e:
        db.rollback()
        print(f"Error clearing data: {e}")


def import_tags(db: Session, tags_data):
    """Import tags from tags.json"""
    print("Importing tags...")
    tag_map = {}

    # Map from category name in JSON to TagCategory enum values
    category_map = {
        "role": TagCategory.ROLE,
        "technology": TagCategory.TECHNOLOGY,
        "skill": TagCategory.SKILL,
        "methodology": TagCategory.METHODOLOGY,
        "tool": TagCategory.TOOL,
    }

    for category_name, tags_list in tags_data.items():
        category_enum = category_map[category_name]

        for tag_name in tags_list:
            tag = Tag(
                name=tag_name,
                category=category_enum,
                description=f"{tag_name} in {category_name} category",
            )
            db.add(tag)
            db.flush()
            tag_map[f"{category_name}:{tag_name}"] = tag

    db.commit()
    print(f"Imported {len(tag_map)} tags")
    return tag_map


def import_jobs(db: Session, jobs_data, tag_map):
    """Import jobs and create job-tag relationships"""
    print("Importing jobs...")
    imported_count = 0

    for job_data in jobs_data:
        try:
            # Parse date
            posting_date = datetime.strptime(
                job_data["job_posting_date"], "%Y-%m-%d"
            ).date()

            # Create job
            job = Job(
                job_id=job_data["job_id"],
                job_position=job_data["job_position"],
                job_link=job_data["job_link"],
                company_name=job_data["company_name"],
                company_profile=job_data.get("company_profile", ""),
                job_location=job_data["job_location"],
                job_posting_date=posting_date,
                tags=job_data["tags"],  # Store original tags as JSON
            )
            db.add(job)
            db.flush()

            # Create job-tag relations
            for category, tag_names in job_data["tags"].items():
                for tag_name in tag_names:
                    tag_key = f"{category}:{tag_name}"
                    if tag_key in tag_map:
                        job_tag = JobTag(job_id=job.id, tag_id=tag_map[tag_key].id)
                        db.add(job_tag)

            imported_count += 1
            if imported_count % 100 == 0:
                db.commit()
                print(f"Imported {imported_count} jobs so far")

        except Exception as e:
            print(f"Error importing job {job_data.get('job_id')}: {e}")
            continue

    db.commit()
    print(f"Imported {imported_count} jobs total")
    return imported_count


def verify_import(conn_details):
    """Verify that data was imported correctly"""
    print("Verifying imported data...")
    # psql_conn = f"PGPASSWORD={conn_details['password']} psql -U {conn_details['user']} -h {conn_details['host']}"

    # job_count_result = run_command(
    #     f"{psql_conn} -d {conn_details['db_name']} -c 'SELECT COUNT(*) FROM jobs'"
    # )
    # tag_count_result = run_command(
    #     f"{psql_conn} -d {conn_details['db_name']} -c 'SELECT COUNT(*) FROM tags'"
    # )
    # job_tag_count_result = run_command(
    #     f"{psql_conn} -d {conn_details['db_name']} -c 'SELECT COUNT(*) FROM job_tags'"
    # )


# MAIN PROCESS
def reset_and_import(num_jobs=500, skip_generate=False):
    """Complete process to reset database and import data"""
    try:
        print("=" * 80)
        print("STARTING DATABASE RESET AND DATA IMPORT")
        print("=" * 80)

        # Step 1: Generate mock data
        if not skip_generate:
            print("\n1. GENERATING MOCK DATA")
            print("-" * 40)
            mock_jobs = generate_mock_jobs(num_jobs)
            save_mock_jobs(mock_jobs)
        else:
            print("\n1. SKIPPING MOCK DATA GENERATION")

        # Step 2: Reset database
        print("\n2. RESETTING DATABASE")
        print("-" * 40)
        conn_details = extract_db_connection_details()
        disconnect_users(conn_details)
        reset_database(conn_details)

        # Step 3: Run migrations
        print("\n3. RUNNING MIGRATIONS")
        print("-" * 40)
        run_migrations()

        # Step 4: Import data
        print("\n4. IMPORTING DATA")
        print("-" * 40)

        # Load data files
        script_dir = os.path.dirname(os.path.abspath(__file__))
        mock_jobs_path = os.path.join(script_dir, "mock_jobs.json")
        tags_path = os.path.join(script_dir, "tags.json")

        with open(mock_jobs_path, "r") as f:
            mock_jobs_data = json.load(f)["jobs"]

        with open(tags_path, "r") as f:
            tags_data = json.load(f)["tags"]

        # Create DB session
        db = SessionLocal()
        try:
            # Import tags then jobs
            tag_map = import_tags(db, tags_data)
            import_jobs(db, mock_jobs_data, tag_map)
        finally:
            db.close()

        # Step 5: Verify import
        print("\n5. VERIFYING IMPORT")
        print("-" * 40)
        verify_import(conn_details)

        print("\n" + "=" * 80)
        print("DATABASE RESET AND DATA IMPORT COMPLETED SUCCESSFULLY")
        print("=" * 80)
        return True

    except Exception as e:
        print(f"\nERROR: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Reset database and import mock data")
    parser.add_argument(
        "--jobs", type=int, default=500, help="Number of jobs to generate"
    )
    parser.add_argument(
        "--skip-generate", action="store_true", help="Skip mock data generation"
    )
    args = parser.parse_args()

    success = reset_and_import(num_jobs=args.jobs, skip_generate=args.skip_generate)
    sys.exit(0 if success else 1)

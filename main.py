import subprocess
from pathlib import Path

print("=" * 60)
print("CareerPulse Job Market Intelligence Pipeline")
print("=" * 60)

scripts = [
    Path("api") / "fetch jobs.py",
    Path("validation_job") / "validate_jobs.py",
    Path("analytics") / "extract_skills.py",
    Path("igestion") / "load_api_to_postgres.py",
    Path("igestion") / "load_skills_to_postgres.py",
]

for script in scripts:

    print(f"\nRunning {script}...\n")

    #result = subprocess.run(["python", script])
    result = subprocess.run(["python", str(script)])

    if result.returncode != 0:

        print(f"❌ Error while executing {script}")

        break

    print(f"✅ {script} completed successfully.")

print("\nPipeline Finished Successfully!")
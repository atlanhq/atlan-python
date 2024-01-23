import os
import json

# Read the test execution times from the JSON file
with open(".test_durations", "r") as f:
    test_durations = json.load(f)

# Accumulate durations for each test file
accumulated_durations = {}
for test, duration in test_durations.items():
    test_file = test.split("::")[0]
    accumulated_durations[test_file] = (
        accumulated_durations.get(test_file, 0) + duration
    )

# Find new test files in the tests/integration directory
integration_test_dir = "tests/integration"
existing_integration_test_files = [
    file
    for file in accumulated_durations.keys()
    if file.startswith(integration_test_dir)
]
new_integration_test_files = [
    file
    for file in os.listdir(integration_test_dir)
    if file.endswith("_test.py") and file not in accumulated_durations
]

# Add new test files to the accumulated durations only if
# they are present in tests/integration directory and not in the ignore list
ignore_list = ["data_mesh_test.py"]
for test_file in new_integration_test_files:
    full_test_file_path = os.path.join(integration_test_dir, test_file)
    if (
        full_test_file_path not in accumulated_durations
        and test_file not in ignore_list
    ):
        accumulated_durations[full_test_file_path] = 0

# Sort test files by accumulated duration in descending order
sorted_test_files = sorted(
    accumulated_durations.items(), key=lambda x: x[1], reverse=True
)

# Distribute test files across multiple parallel jobs while balancing execution time
num_jobs = 20  # Adjust the number of parallel jobs as needed
jobs = {f"job{i+1}": {"test_files": [], "total_time": 0} for i in range(num_jobs)}

for test_file, duration in sorted_test_files:
    # Skip test files in the ignore list
    if test_file in ignore_list:
        continue

    # Find the job with the least total execution time
    min_job = min(jobs, key=lambda j: jobs[j]["total_time"])

    # Add the test file to the selected job
    jobs[min_job]["test_files"].append(test_file)

    # Update the total execution time for the selected job
    jobs[min_job]["total_time"] += duration

# Output the distributed test files for each job with total time in seconds and minutes
result = {
    f"{job}": {
        "test_files": jobs[job]["test_files"],
        "total_time_seconds": jobs[job]["total_time"],
        "total_time_minutes": jobs[job]["total_time"] / 60,
    }
    for job in jobs
}
print(json.dumps(result, indent=2))

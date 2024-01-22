import json

# Read the test execution times from the JSON file
with open('.sample', 'r') as f:
    test_durations = json.load(f)

# Accumulate durations for each test file
accumulated_durations = {}
for test, duration in test_durations.items():
    test_file = test.split('::')[0]
    accumulated_durations[test_file] = accumulated_durations.get(test_file, 0) + duration

# Sort test files by accumulated duration in descending order
sorted_test_files = sorted(accumulated_durations.items(), key=lambda x: x[1], reverse=True)

# Distribute test files across multiple parallel jobs while balancing execution time
num_jobs = 2  # Adjust the number of parallel jobs as needed
jobs = {f'job{i+1}': {'test_files': [], 'total_time': 0} for i in range(num_jobs)}

for test_file, duration in sorted_test_files:
    # Find the job with the least total execution time
    min_job = min(jobs, key=lambda j: jobs[j]['total_time'])
    
    # Add the test file to the selected job
    jobs[min_job]['test_files'].append(test_file)
    
    # Update the total execution time for the selected job
    jobs[min_job]['total_time'] += duration

# Output the distributed test files for each job with total time in seconds and minutes
result = {f'{job}': {'test_files': jobs[job]['test_files'], 'total_time_seconds': jobs[job]['total_time'], 'total_time_minutes': jobs[job]['total_time'] / 60} for job in jobs}
print(json.dumps(result, indent=2))

#####!/usr/bin/python3
# condor_job_script.py
import sys
import numpy as np
import os

# --- Common Simulation Parameters (copied for self-containment in each job) ---
R_MIN = 0.0
R_MAX = 4.0
NUM_R_VALUES_TOTAL = 5000 
INITIAL_X = 0.5
WARMUP_ITERATIONS = 1000
PLOT_ITERATIONS = 100
OUTPUT_DIR = "bifurcation_data" 

def sine_map(x, r):
    """The sine map equation: x_{n+1} = r * sin(x_n)"""
    return r * np.sin(x)

def simulate_single_r(r_value, initial_x, warmup_iterations, plot_iterations):
    """
    Simulates the map for a single r value and returns its long-term x values.
    """
    x = initial_x
    
    # Warm-up iterations to discard transients
    for _ in range(warmup_iterations):
        x = sine_map(x, r_value)
    
    # Plotting iterations to capture the attractor
    x_for_plot = []
    for _ in range(plot_iterations):
        x = sine_map(x, r_value)
        x_for_plot.append(x)
        
    return r_value, np.array(x_for_plot) # Return r_value and x_values as a NumPy array

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python condor_job_script.py <process_id> <total_jobs>")
        sys.exit(1)

    process_id = int(sys.argv[1])
    total_jobs = int(sys.argv[2])

    print(f"Starting job {process_id} of {total_jobs}...")

    # Calculate the full range of r values
    all_r_values = np.linspace(R_MIN, R_MAX, NUM_R_VALUES_TOTAL)

    # Determine which r values this specific job will process
    # Using a stride to distribute values evenly across jobs
    # E.g., job 0 gets 0, 20, 40...; job 1 gets 1, 21, 41... (if total_jobs=20)
    r_chunk_for_this_job = all_r_values[process_id::total_jobs]

    print(f"Job {process_id}: Processing {len(r_chunk_for_this_job)} r values.")

    # Lists to store results for this job
    job_r_data = []
    job_x_data = []

    for r_val in r_chunk_for_this_job:
        r_current, x_current_attractor = simulate_single_r(
            r_val, INITIAL_X, WARMUP_ITERATIONS, PLOT_ITERATIONS
        )
        # Extend with r_val for each x_point to make plotting easier later
        job_r_data.extend([r_current] * len(x_current_attractor))
        job_x_data.extend(x_current_attractor)

    # Ensure output directory exists
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Save results to a unique file for this job
    output_filename = os.path.join(OUTPUT_DIR, f"results_{process_id}.npz")
    np.savez_compressed(output_filename, r=np.array(job_r_data), x=np.array(job_x_data))

    print(f"Job {process_id} finished. Results saved to {output_filename}")

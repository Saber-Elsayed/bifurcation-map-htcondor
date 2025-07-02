# gather_and_plot.py
import numpy as np
import matplotlib.pyplot as plt
import os
import glob

# --- Common Simulation Parameters (copied for self-containment) ---
R_MIN = 0.0
R_MAX = 4.0
NUM_R_VALUES_TOTAL = 5000 
INITIAL_X = 0.5
WARMUP_ITERATIONS = 1000
PLOT_ITERATIONS = 100
NUM_HTCONDOR_JOBS = 500 # Needs to match the number of jobs submitted
OUTPUT_DIR = "bifurcation_data" 

if __name__ == "__main__":
    print(f"Gathering data from {OUTPUT_DIR}/...")
    
    all_r_data = []
    all_x_data = []

    # Use glob to find all result files
    # Make sure you expect 'NUM_HTCONDOR_JOBS' files. 
    # If a job fails, its file might be missing.
    result_files = glob.glob(os.path.join(OUTPUT_DIR, "results_*.npz"))
    
    if not result_files:
        print(f"No result files found in {OUTPUT_DIR}. Make sure HTCondor jobs completed.")
        print("Expected files like: results_0.npz, results_1.npz, ...")
        exit()

    # Sort files by their process ID to ensure correct order if needed (though not strictly necessary for plotting)
    result_files.sort(key=lambda f: int(os.path.basename(f).split('_')[1].split('.')[0]))

    for filepath in result_files:
        try:
            data = np.load(filepath)
            all_r_data.extend(data['r'].tolist()) # .tolist() converts numpy array to list for extend
            all_x_data.extend(data['x'].tolist())
            print(f"Loaded {filepath}")
        except Exception as e:
            print(f"Error loading {filepath}: {e}")

    if not all_r_data or not all_x_data:
        print("No data collected for plotting. Exiting.")
        exit()

    print(f"Total data points collected: {len(all_r_data)}")
    print("Plotting bifurcation map...")

    # --- Plotting ---
    plt.figure(figsize=(12, 8))
    # Use ',' for dots (pixels), 'k' for black, alpha for transparency.
    # markersize=0.1 makes the dots very small, almost like a continuous line for dense regions.
    plt.plot(all_r_data, all_x_data, ',k', alpha=0.5, markersize=0.1) 
    plt.title(r'Bifurcation Map of $x_{n+1} = r \cdot \sin(x_n)$ (HTCondor Distributed)')
    plt.xlabel('Parameter $r$')
    plt.ylabel('$x_{n+1}$ values (long-term behavior)')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.show()
    print("Plot generated successfully.")

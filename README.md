# bifurcation-map-htcondor

## Project Overview
This project performs distributed bifurcation calculations using HTCondor and Python. It includes:
- `condor_job_script.py`: Runs bifurcation calculations for different parameters.
- `gather_and_plot.py`: Collects results and generates a bifurcation map plot.

## Requirements
- Python 3.12 or higher
- HTCondor (for distributed job execution)

## Setup Instructions

### 1. Clone the repository
```bash
git clone <repo-url>
cd bifurcation-map-htcondor
```

### 2. Create and activate a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```
If you do not have a `requirements.txt` file, install manually:
```bash
pip install numpy matplotlib PyQt5
```

## Running the Project

### 1. Prepare directories
Make sure the following directories exist in the project root:
- `bifurcation_data` (for calculation results)
- `log` (for HTCondor log files)

### 2. Submit jobs with HTCondor
Prepare a submit file for HTCondor to run `condor_job_script.py` with different parameters. Submit jobs using:
```bash
condor_submit <your_submit_file>
```

### 3. Gather and plot results
After all jobs are complete, run:
```bash
python gather_and_plot.py
```
This will generate the bifurcation map plot from the results.

## Deactivating the Virtual Environment
To exit the virtual environment, simply run:
```bash
deactivate
```

## Notes
- Do **not** include the `venv` directory when submitting or pushing to GitHub.
- Make sure to provide a `requirements.txt` for reproducibility.
- For any issues, please refer to the assignment instructions or contact the course staff.

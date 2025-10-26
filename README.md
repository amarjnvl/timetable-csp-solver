# Timetable CSP Solver - AI Course Scheduling System

**Course:** CSMI17 – Artificial Intelligence  
**Assignment:** Question 2 - Timetable Generation as Constraint Satisfaction Problem  
**Author:** AMAR KUMAR
**GitHub:** `timetable-csp-solver`

## Overview

Automated timetable generation system using two CSP solving approaches:
1. **Backtracking with Heuristics** (MRV + LCV)
2. **Backtracking with Forward Checking**

Compares algorithm performance on course scheduling with conflicting constraints.

---

## Problem Definition

**Objective:** Assign courses to (timeslot, room) pairs satisfying all constraints.

**Variables:** Courses requiring assignment  
**Domain:** All (timeslot, room) combinations  
**Constraints:**
- No room double-booking
- Instructor cannot teach multiple courses simultaneously  
- Instructor availability restrictions
- Room type requirements (lab/classroom)
- Course time preferences (creates conflicts)

---

## Quick Start Guide

### For New Users Opening This Repository

#### 1. Prerequisites
- **Python 3.8+** installed ([Download](https://www.python.org/downloads/))
- **PowerShell** (Windows) or Terminal (Mac/Linux)
- **Git** (optional, for cloning)

#### 2. Get the Code

**Option A: Clone with Git**
```powershell
git clone https://github.com/amarjnvl/timetable-csp-solver.git
cd timetable-csp-solver
```

**Option B: Download ZIP**
- Click green "Code" button → "Download ZIP"
- Extract to folder
- Open PowerShell in that folder:
```powershell
cd path\to\timetable-csp-solver
```

#### 3. Setup Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate it
.\venv\Scripts\Activate.ps1

# If you get execution policy error:
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
pip install -r requirements.txt
```

**Verify setup:**
```powershell
python --version    # Should show Python 3.8+
pip list           # Should show matplotlib, pandas, numpy, tabulate
```

#### 4. Run the Program

```powershell
python main.py
```

**Expected output:** Console shows experiment progress, timetables, and metrics. Files saved to `output/` directory.

#### 5. View Results

```powershell
# Open graphs folder
explorer output\graphs

# View JSON timetable
Get-Content output\results\small_problem_heuristics.json

# List all outputs
dir output\results
dir output\graphs
```

---

## Project Structure

```
timetable-csp-solver/
├── src/
│   ├── models/
│   │   ├── timetable.py          # CSP data structures (Course, TimeSlot, Room)
│   │   └── constraints.py         # Constraint validation logic
│   ├── solvers/
│   │   ├── backtracking_heuristics.py        # MRV + LCV implementation
│   │   └── backtracking_forward_checking.py  # Forward checking implementation
│   └── utils/
│       ├── generator.py           # Problem instance generator
│       └── visualizer.py          # Output formatting & graphs
├── output/
│   ├── results/                   # JSON timetables (6 files)
│   └── graphs/                    # Performance comparisons (3 PNG files)
├── tests/
│   └── test_solvers.py           # Unit tests
├── main.py                        # Main execution script
├── requirements.txt               # Python dependencies
├── README.md                      # This file
└── .gitignore                     # Git exclusions
```

---

## Algorithm Details

### Method 1: Backtracking with Heuristics

**MRV (Minimum Remaining Values):**
- Selects course with fewest valid assignments
- Fails fast on impossible branches

**LCV (Least Constraining Value):**
- Orders values by least impact on other variables
- Preserves maximum flexibility

**Performance:** Smarter search, fewer nodes explored

### Method 2: Backtracking with Forward Checking

**Forward Checking:**
- After each assignment, prunes inconsistent values from unassigned variables
- Detects dead-ends early via domain wipeout
- Maintains arc consistency

**Performance:** More pruning, can explore more nodes but detects failures earlier

---

## Output Files

### JSON Timetables (`output/results/`)

Six files generated:
- `small_problem_heuristics.json`
- `small_problem_forward_checking.json`
- `medium_problem_heuristics.json`
- `medium_problem_forward_checking.json`
- `complex_problem_heuristics.json`
- `complex_problem_forward_checking.json`

**Format:**
```json
[
  {
    "course_id": "CS101",
    "course_name": "Data Structures",
    "instructor": "Dr. Smith",
    "day": "Monday",
    "period": 1,
    "room": "R201"
  }
]
```

### Performance Graphs (`output/graphs/`)

Three comparison charts (4 subplots each):
1. **Nodes Explored** - Search space coverage
2. **Backtracks** - Failed assignment attempts
3. **Time Taken** - Execution speed
4. **Values Pruned** - Forward checking efficiency

---

## Customization

### Modify Problem Size

Edit `main.py`:
```python
small_problem = TimetableGenerator.generate_sample_problem(
    num_courses=8,      # Change number of courses
    num_rooms=2,        # Change available rooms
    num_days=5,         # Days per week
    periods_per_day=6   # Periods per day
)
```

### Add Constraints

Edit `src/models/constraints.py` in `check_all_constraints()` method:
```python
# Add custom constraint
if your_custom_condition:
    return False
```

### Modify Instructor Availability

Edit `src/utils/generator.py`:
```python
instructor_constraints = {
    "Dr. Smith": ["Friday", "Thursday"],  # Unavailable days
    "Dr. Johnson": ["Wednesday"],
    # Add more instructors...
}
```

### Adjust Course Preferences

Edit `src/utils/generator.py`:
```python
preferred_times = {
    "CS101": [("Monday", 1)],        # Preferred slots
    "CS102": [("Monday", 1)],        # Creates conflict
    # Add more courses...
}
```

---

## Testing

Run unit tests:
```powershell
python tests\test_solvers.py
```

Or with pytest (if installed):
```powershell
pytest tests/
```

---

## Troubleshooting

### "No module named 'src'"
```powershell
# Ensure you're in project root
cd timetable-csp-solver
python main.py
```

### Virtual Environment Won't Activate
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\venv\Scripts\Activate.ps1
```

### "No solution found"
- Expected behavior for small/medium problems (demonstrates backtracking)
- Over-constrained by design to show algorithm differences
- Complex problem always finds solution

### Missing Output Files
```powershell
mkdir output\results -Force
mkdir output\graphs -Force
python main.py
```

---

## Performance Metrics Explained

**Nodes Explored:** Total variables assigned during search  
**Backtracks:** Times algorithm undid assignments (failures)  
**Pruned Values:** Domain reductions (forward checking only)  
**Time Taken:** Wall-clock execution time  
**Success:** Whether valid timetable was found

**Expected Results:**
- Small/Medium: No solution, but shows backtracking behavior
- Complex: Solution found
- Forward Checking: More nodes but better pruning
- Heuristics: Fewer nodes via smart ordering

---

## GitHub Repository Setup

### Recommended Repository Name
```
timetable-csp-solver
```
or
```
ai-timetable-scheduling
```

### Initialization Commands

```powershell
# In project directory
git init
git add .
git commit -m "Initial commit: Timetable CSP solver with two backtracking methods"

# Create repo on GitHub, then:
git remote add origin https://github.com/amarjnvl/timetable-csp-solver.git
git branch -M main
git push -u origin main
```

### .gitignore Included
Automatically excludes:
- Virtual environment (`venv/`)
- Python cache (`__pycache__/`)
- Output files (structure preserved)
- IDE files

---

## Assignment Report Checklist

Use outputs for report:

✓ **Problem Definition** - See "Problem Definition" section above  
✓ **Assumptions** - See "Customization" section for constraint details  
✓ **Algorithm Descriptions** - See "Algorithm Details" section  
✓ **Experimental Setup** - Screenshot console output + problem sizes  
✓ **Performance Comparison** - Use PNG graphs from `output/graphs/`  
✓ **GitHub Link** - Include repository URL

---

## Technical Specifications

**Language:** Python 3.8+  
**Dependencies:**
- matplotlib 3.8.2 (graphs)
- pandas 2.1.4 (data handling)
- numpy 1.26.3 (numerical operations)
- tabulate 0.9.0 (formatted tables)

**Algorithms Implemented:**
- Backtracking search
- MRV heuristic
- LCV heuristic  
- Forward checking with domain pruning
- Constraint propagation

---

## Clean & Re-run

```powershell
# Delete previous results
Remove-Item output\results\* -Force
Remove-Item output\graphs\* -Force

# Run fresh
python main.py
```

---

## Exit Virtual Environment

```powershell
deactivate
```

---

## License

Academic project for CSMI17 - Artificial Intelligence course.

---

## Support

For issues or questions:
1. Check "Troubleshooting" section
2. Verify setup with `python --version` and `pip list`
3. Ensure all files from repository are present
4. Check that virtual environment is activated (see `(venv)` in prompt)

---

## Summary for Quick Reference

```powershell
# Setup (once)
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Run (every time)
python main.py

# View results
explorer output\graphs
Get-Content output\results\small_problem_heuristics.json
```

**Expected Runtime:** 2-5 seconds for all three experiments  
**Output:** 6 JSON files + 3 PNG graphs + console logs
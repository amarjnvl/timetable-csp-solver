#!/usr/bin/env python3
"""
Timetable Generation as Constraint Satisfaction Problem (CSP)
Compares two backtracking approaches:
1. Backtracking with Variable/Value Ordering Heuristics (MRV + LCV)
2. Backtracking with Forward Checking
"""

import os
from src.models.timetable import TimetableProblem
from src.solvers.backtracking_heuristics import BacktrackingWithHeuristics
from src.solvers.backtracking_forward_checking import BacktrackingWithForwardChecking
from src.utils.generator import TimetableGenerator
from src.utils.visualizer import TimetableVisualizer

def ensure_output_dirs():
    """Create output directories if they don't exist"""
    os.makedirs('output/results', exist_ok=True)
    os.makedirs('output/graphs', exist_ok=True)

def run_experiment(problem: TimetableProblem, experiment_name: str):
    """Run both solvers and compare performance"""
    
    print("\n" + "="*100)
    print(f"EXPERIMENT: {experiment_name}".center(100))
    print("="*100 + "\n")
    
    print(f"Problem Size:")
    print(f"  - Courses: {len(problem.courses)}")
    print(f"  - Timeslots: {len(problem.timeslots)}")
    print(f"  - Rooms: {len(problem.rooms)}")
    print(f"  - Total possible assignments: {len(problem.timeslots) * len(problem.rooms)}")
    print()
    
    # Solver 1: Backtracking with Heuristics
    print("Running Solver 1: Backtracking with MRV + LCV Heuristics...")
    solver1 = BacktrackingWithHeuristics(problem)
    solution1, metrics1 = solver1.solve()
    
    if solution1:
        print("✓ Solution found!")
        TimetableVisualizer.print_timetable(solution1)
        TimetableVisualizer.save_timetable_to_file(
            solution1, 
            f'output/results/{experiment_name}_heuristics.json'
        )
    else:
        print("✗ No solution found!")
    
    print()
    
    # Solver 2: Backtracking with Forward Checking
    print("Running Solver 2: Backtracking with Forward Checking...")
    solver2 = BacktrackingWithForwardChecking(problem)
    solution2, metrics2 = solver2.solve()
    
    if solution2:
        print("✓ Solution found!")
        TimetableVisualizer.print_timetable(solution2)
        TimetableVisualizer.save_timetable_to_file(
            solution2, 
            f'output/results/{experiment_name}_forward_checking.json'
        )
    else:
        print("✗ No solution found!")
    
    print()
    
    # Performance Comparison
    labels = ['Heuristics (MRV+LCV)', 'Forward Checking']
    metrics_list = [metrics1, metrics2]
    
    TimetableVisualizer.print_metrics_table(metrics_list, labels)
    TimetableVisualizer.plot_performance_comparison(
        metrics_list, 
        labels,
        f'output/graphs/{experiment_name}_comparison.png'
    )
    
    print(f"\nExperiment '{experiment_name}' completed!\n")
    return metrics1, metrics2

def main():
    """Main execution function"""
    
    print("\n" + "="*100)
    print("TIMETABLE GENERATION - CONSTRAINT SATISFACTION PROBLEM".center(100))
    print("="*100 + "\n")
    
    ensure_output_dirs()
    
    # Experiment 1: Small Problem
    print("\n--- GENERATING SMALL PROBLEM ---")
    small_problem = TimetableGenerator.generate_sample_problem(
        num_courses=8,
        num_rooms=2,
        num_days=5,
        periods_per_day=6
    )
    run_experiment(small_problem, "small_problem")
    
    # Experiment 2: Medium Problem
    print("\n--- GENERATING MEDIUM PROBLEM ---")
    medium_problem = TimetableGenerator.generate_sample_problem(
        num_courses=10,
        num_rooms=2,
        num_days=5,
        periods_per_day=6
    )
    run_experiment(medium_problem, "medium_problem")
    
    # Experiment 3: Complex Problem
    print("\n--- GENERATING COMPLEX PROBLEM ---")
    complex_problem = TimetableGenerator.generate_complex_problem()
    run_experiment(complex_problem, "complex_problem")
    
    print("\n" + "="*100)
    print("ALL EXPERIMENTS COMPLETED".center(100))
    print("="*100)
    print("\nResults saved in:")
    print("  - output/results/  (JSON timetables)")
    print("  - output/graphs/   (Performance comparisons)")
    print()

if __name__ == "__main__":
    main()
"""
Unit tests for timetable solvers
Run with: python -m pytest tests/test_solvers.py
"""

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.models.timetable import Course, TimeSlot, Room, TimetableProblem
from src.solvers.backtracking_heuristics import BacktrackingWithHeuristics
from src.solvers.backtracking_forward_checking import BacktrackingWithForwardChecking
from src.utils.generator import TimetableGenerator

def test_small_problem_heuristics():
    """Test heuristics solver on small problem"""
    problem = TimetableGenerator.generate_sample_problem(num_courses=4, num_rooms=3)
    solver = BacktrackingWithHeuristics(problem)
    solution, metrics = solver.solve()
    
    assert solution is not None, "Should find solution for small problem"
    assert len(solution) == len(problem.variables), "Should assign all courses"
    assert metrics['success'] == True

def test_small_problem_forward_checking():
    """Test forward checking solver on small problem"""
    problem = TimetableGenerator.generate_sample_problem(num_courses=4, num_rooms=3)
    solver = BacktrackingWithForwardChecking(problem)
    solution, metrics = solver.solve()
    
    assert solution is not None, "Should find solution for small problem"
    assert len(solution) == len(problem.variables), "Should assign all courses"
    assert metrics['success'] == True

def test_constraint_satisfaction():
    """Test that solutions satisfy all constraints"""
    problem = TimetableGenerator.generate_sample_problem(num_courses=5, num_rooms=3)
    solver = BacktrackingWithHeuristics(problem)
    solution, _ = solver.solve()
    
    if solution:
        # Check no room conflicts
        timeslot_room_pairs = {}
        for course, (timeslot, room) in solution.items():
            key = (timeslot.day, timeslot.period, room.id)
            assert key not in timeslot_room_pairs, "Room conflict detected"
            timeslot_room_pairs[key] = course
        
        # Check no instructor conflicts
        instructor_timeslots = {}
        for course, (timeslot, room) in solution.items():
            key = (course.instructor, timeslot.day, timeslot.period)
            assert key not in instructor_timeslots, "Instructor conflict detected"
            instructor_timeslots[key] = course

def test_metrics_collected():
    """Test that both solvers collect metrics"""
    problem = TimetableGenerator.generate_sample_problem(num_courses=4, num_rooms=3)
    
    # Test heuristics
    solver1 = BacktrackingWithHeuristics(problem)
    _, metrics1 = solver1.solve()
    assert 'nodes_explored' in metrics1
    assert 'backtracks' in metrics1
    assert 'time_taken' in metrics1
    
    # Test forward checking
    solver2 = BacktrackingWithForwardChecking(problem)
    _, metrics2 = solver2.solve()
    assert 'nodes_explored' in metrics2
    assert 'pruned_values' in metrics2

if __name__ == "__main__":
    print("Running tests...")
    test_small_problem_heuristics()
    print("✓ Heuristics solver test passed")
    
    test_small_problem_forward_checking()
    print("✓ Forward checking solver test passed")
    
    test_constraint_satisfaction()
    print("✓ Constraint satisfaction test passed")
    
    test_metrics_collected()
    print("✓ Metrics collection test passed")
    
    print("\nAll tests passed!")
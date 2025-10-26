from typing import Dict, Tuple, List, Optional
from ..models.timetable import Course, TimeSlot, Room, TimetableProblem
from ..models.constraints import ConstraintChecker
import time

class BacktrackingWithHeuristics:
    def __init__(self, problem: TimetableProblem):
        self.problem = problem
        self.nodes_explored = 0
        self.backtracks = 0
        self.start_time = 0
        self.end_time = 0
    
    def solve(self) -> Tuple[Optional[Dict[Course, Tuple[TimeSlot, Room]]], Dict]:
        """Solve using backtracking with MRV and LCV heuristics"""
        self.nodes_explored = 0
        self.backtracks = 0
        self.start_time = time.time()
        
        assignment = {}
        result = self._backtrack(assignment)
        
        self.end_time = time.time()
        
        metrics = {
            'nodes_explored': self.nodes_explored,
            'backtracks': self.backtracks,
            'time_taken': self.end_time - self.start_time,
            'success': result is not None
        }
        
        return result, metrics
    
    def _backtrack(self, assignment: Dict[Course, Tuple[TimeSlot, Room]]) -> Optional[Dict]:
        """Recursive backtracking with heuristics"""
        
        if ConstraintChecker.is_complete(self.problem, assignment):
            return assignment
        
        # Variable ordering: Minimum Remaining Values (MRV)
        course = self._select_unassigned_variable_mrv(assignment)
        self.nodes_explored += 1
        
        # Value ordering: Least Constraining Value (LCV)
        ordered_values = self._order_domain_values_lcv(course, assignment)
        
        for timeslot, room in ordered_values:
            if ConstraintChecker.check_all_constraints(self.problem, assignment, 
                                                      course, timeslot, room):
                assignment[course] = (timeslot, room)
                
                result = self._backtrack(assignment)
                if result is not None:
                    return result
                
                # Backtrack
                del assignment[course]
                self.backtracks += 1
        
        return None
    
    def _select_unassigned_variable_mrv(self, assignment: Dict) -> Course:
        """Select variable with Minimum Remaining Values"""
        unassigned = [c for c in self.problem.variables if c not in assignment]
        
        # Count valid values for each unassigned course
        min_values = float('inf')
        selected_course = None
        
        for course in unassigned:
            valid_count = 0
            for timeslot, room in self.problem.get_domain(course):
                if ConstraintChecker.check_all_constraints(self.problem, assignment,
                                                          course, timeslot, room):
                    valid_count += 1
            
            if valid_count < min_values:
                min_values = valid_count
                selected_course = course
        
        return selected_course if selected_course else unassigned[0]
    
    def _order_domain_values_lcv(self, course: Course, 
                                 assignment: Dict) -> List[Tuple[TimeSlot, Room]]:
        """Order domain values by Least Constraining Value"""
        domain = self.problem.get_domain(course)
        
        # Filter valid values
        valid_values = [(ts, r) for ts, r in domain 
                       if ConstraintChecker.check_all_constraints(self.problem, assignment,
                                                                 course, ts, r)]
        
        # Count constraints imposed by each value
        value_constraints = []
        for timeslot, room in valid_values:
            constraints_count = self._count_constraints(course, timeslot, room, assignment)
            value_constraints.append(((timeslot, room), constraints_count))
        
        # Sort by least constraining (lowest count)
        value_constraints.sort(key=lambda x: x[1])
        
        return [val for val, _ in value_constraints]
    
    def _count_constraints(self, course: Course, timeslot: TimeSlot, 
                          room: Room, assignment: Dict) -> int:
        """Count how many future assignments this value would constrain"""
        count = 0
        unassigned = [c for c in self.problem.variables if c not in assignment and c != course]
        
        # Temporarily assign
        temp_assignment = assignment.copy()
        temp_assignment[course] = (timeslot, room)
        
        for other_course in unassigned:
            for other_ts, other_room in self.problem.get_domain(other_course):
                if not ConstraintChecker.check_all_constraints(self.problem, temp_assignment,
                                                              other_course, other_ts, other_room):
                    count += 1
        
        return count
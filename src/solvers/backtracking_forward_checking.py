from typing import Dict, Tuple, List, Optional, Set
from ..models.timetable import Course, TimeSlot, Room, TimetableProblem
from ..models.constraints import ConstraintChecker
import time
import copy

class BacktrackingWithForwardChecking:
    def __init__(self, problem: TimetableProblem):
        self.problem = problem
        self.nodes_explored = 0
        self.backtracks = 0
        self.pruned_values = 0
        self.start_time = 0
        self.end_time = 0
    
    def solve(self) -> Tuple[Optional[Dict[Course, Tuple[TimeSlot, Room]]], Dict]:
        """Solve using backtracking with forward checking"""
        self.nodes_explored = 0
        self.backtracks = 0
        self.pruned_values = 0
        self.start_time = time.time()
        
        # Initialize domains
        domains = {course: list(self.problem.get_domain(course)) 
                  for course in self.problem.variables}
        
        assignment = {}
        result = self._backtrack(assignment, domains)
        
        self.end_time = time.time()
        
        metrics = {
            'nodes_explored': self.nodes_explored,
            'backtracks': self.backtracks,
            'pruned_values': self.pruned_values,
            'time_taken': self.end_time - self.start_time,
            'success': result is not None
        }
        
        return result, metrics
    
    def _backtrack(self, assignment: Dict[Course, Tuple[TimeSlot, Room]], 
                   domains: Dict[Course, List[Tuple[TimeSlot, Room]]]) -> Optional[Dict]:
        """Recursive backtracking with forward checking"""
        
        if ConstraintChecker.is_complete(self.problem, assignment):
            return assignment
        
        # Select unassigned variable
        course = self._select_unassigned_variable(assignment, domains)
        self.nodes_explored += 1
        
        for timeslot, room in list(domains[course]):
            if ConstraintChecker.check_all_constraints(self.problem, assignment, 
                                                      course, timeslot, room):
                assignment[course] = (timeslot, room)
                
                # Forward checking: prune inconsistent values
                removed_values = self._forward_check(course, timeslot, room, 
                                                     assignment, domains)
                
                if removed_values is not None:  # No domain wipeout
                    result = self._backtrack(assignment, domains)
                    if result is not None:
                        return result
                
                # Restore removed values
                if removed_values is not None:
                    self._restore_domains(domains, removed_values)
                
                # Backtrack
                del assignment[course]
                self.backtracks += 1
        
        return None
    
    def _select_unassigned_variable(self, assignment: Dict, 
                                   domains: Dict) -> Course:
        """Select unassigned variable (can use heuristics or simple order)"""
        unassigned = [c for c in self.problem.variables if c not in assignment]
        
        # Simple MRV: select variable with smallest domain
        return min(unassigned, key=lambda c: len(domains[c]))
    
    def _forward_check(self, assigned_course: Course, timeslot: TimeSlot, 
                      room: Room, assignment: Dict, 
                      domains: Dict) -> Optional[Dict[Course, List[Tuple]]]:
        """
        Forward checking: remove inconsistent values from domains of unassigned variables
        Returns dict of removed values, or None if domain wipeout occurs
        """
        removed = {course: [] for course in self.problem.variables}
        
        for course in self.problem.variables:
            if course in assignment:
                continue
            
            to_remove = []
            for ts, r in domains[course]:
                # Check if this value is now inconsistent
                temp_assignment = assignment.copy()
                temp_assignment[course] = (ts, r)
                
                # Check conflicts with newly assigned course
                if assigned_course.instructor == course.instructor and ts == timeslot:
                    to_remove.append((ts, r))
                    self.pruned_values += 1
                elif ts == timeslot and r == room:
                    to_remove.append((ts, r))
                    self.pruned_values += 1
            
            # Remove inconsistent values
            for val in to_remove:
                domains[course].remove(val)
                removed[course].append(val)
            
            # Check for domain wipeout
            if len(domains[course]) == 0:
                return None
        
        return removed
    
    def _restore_domains(self, domains: Dict, 
                        removed: Dict[Course, List[Tuple]]):
        """Restore previously removed values to domains"""
        for course, values in removed.items():
            domains[course].extend(values)
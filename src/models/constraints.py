from typing import Dict, Tuple
from .timetable import Course, TimeSlot, Room, TimetableProblem

class ConstraintChecker:
    @staticmethod
    def check_all_constraints(problem: TimetableProblem, 
                             assignment: Dict[Course, Tuple[TimeSlot, Room]],
                             course: Course, 
                             timeslot: TimeSlot, 
                             room: Room) -> bool:
        """Check if assigning (timeslot, room) to course violates any constraint"""
        
        # 1. No two courses can occupy the same room at the same time
        if not ConstraintChecker._check_room_conflict(assignment, timeslot, room):
            return False
        
        # 2. Instructor cannot teach two courses at the same time
        if not ConstraintChecker._check_instructor_conflict(assignment, course, timeslot):
            return False
        
        # 3. Instructor availability constraint
        unavailable = problem.instructor_constraints.get(course.instructor, [])
        if timeslot.day in unavailable:
            return False
        
        # Preference constraint
        if course.id in problem.preferred_times:
            prefs = problem.preferred_times[course.id]
            if not any((timeslot.day == day and timeslot.period == period) for day, period in prefs):
                return False
        
        return True
    
    @staticmethod
    def _check_room_conflict(assignment: Dict[Course, Tuple[TimeSlot, Room]], 
                            timeslot: TimeSlot, room: Room) -> bool:
        """Check if room is already occupied at this timeslot"""
        for assigned_course, (assigned_slot, assigned_room) in assignment.items():
            if assigned_slot == timeslot and assigned_room == room:
                return False
        return True
    
    @staticmethod
    def _check_instructor_conflict(assignment: Dict[Course, Tuple[TimeSlot, Room]], 
                                  course: Course, timeslot: TimeSlot) -> bool:
        """Check if instructor is already teaching at this timeslot"""
        for assigned_course, (assigned_slot, _) in assignment.items():
            if (assigned_course.instructor == course.instructor and 
                assigned_slot == timeslot):
                return False
        return True
    
    @staticmethod
    def is_complete(problem: TimetableProblem, 
                   assignment: Dict[Course, Tuple[TimeSlot, Room]]) -> bool:
        """Check if all courses are assigned"""
        return len(assignment) == len(problem.variables)
# src/models/__init__.py
"""Data models for timetable CSP"""
from .timetable import Course, TimeSlot, Room, TimetableProblem, TimetableAssignment
from .constraints import ConstraintChecker

__all__ = ['Course', 'TimeSlot', 'Room', 'TimetableProblem', 'TimetableAssignment', 'ConstraintChecker']

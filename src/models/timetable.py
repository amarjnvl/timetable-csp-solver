from typing import List, Dict, Set, Tuple
from dataclasses import dataclass

@dataclass(frozen=True)
class Course:
    id: str
    name: str
    instructor: str
    duration: int  # in hours per week
    
    def __repr__(self):
        return f"{self.id}-{self.name}"

@dataclass
class TimeSlot:
    day: str
    period: int  # 1-8 (assuming 8 periods per day)
    
    def __repr__(self):
        return f"{self.day}-P{self.period}"
    
    def __hash__(self):
        return hash((self.day, self.period))
    
    def __eq__(self, other):
        return self.day == other.day and self.period == other.period

@dataclass(frozen=True)
class Room:
    id: str
    capacity: int
    type: str  # 'lab' or 'classroom'
    
    def __repr__(self):
        return f"{self.id}"

class TimetableAssignment:
    def __init__(self, course: Course, timeslot: TimeSlot, room: Room):
        self.course = course
        self.timeslot = timeslot
        self.room = room
    
    def __repr__(self):
        return f"{self.course.id} | {self.timeslot} | {self.room.id}"

class TimetableProblem:
    def __init__(self, courses: List[Course], timeslots: List[TimeSlot], 
                rooms: List[Room], instructor_constraints: Dict[str, List[str]],
                preferred_times: Dict[str, List[Tuple[str, int]]] = None):
        self.courses = courses
        self.timeslots = timeslots
        self.rooms = rooms
        self.instructor_constraints = instructor_constraints
        self.preferred_times = preferred_times or {}
        
        # Variables: each course needs to be assigned
        self.variables = courses
        
        # Domain: each course can be assigned to (timeslot, room) pairs
        self.domains = self._initialize_domains()
    
    def _initialize_domains(self) -> Dict[Course, List[Tuple[TimeSlot, Room]]]:
        domains = {}
        for course in self.courses:
            valid_assignments = []
            for timeslot in self.timeslots:
                for room in self.rooms:
                    # Basic domain filtering
                    if self._is_valid_domain(course, timeslot, room):
                        valid_assignments.append((timeslot, room))
            domains[course] = valid_assignments
        return domains
    
    def _is_valid_domain(self, course: Course, timeslot: TimeSlot, room: Room) -> bool:
        # Check if instructor is available
        unavailable_days = self.instructor_constraints.get(course.instructor, [])
        if timeslot.day in unavailable_days:
            return False
        
        # Check if room type matches course requirement (simple heuristic)
        # Assume courses with 'Lab' in name need lab rooms
        if 'Lab' in course.name and room.type != 'lab':
            return False
        
        return True
    
    def get_domain(self, course: Course) -> List[Tuple[TimeSlot, Room]]:
        return self.domains[course]
from typing import List, Dict
from ..models.timetable import Course, TimeSlot, Room, TimetableProblem

class TimetableGenerator:
    @staticmethod
    def generate_sample_problem(num_courses: int = 8, 
                               num_rooms: int = 4,
                               num_days: int = 5,
                               periods_per_day: int = 6) -> TimetableProblem:
        """Generate a sample timetable problem"""
        
        # Generate courses
        courses = []
        course_names = [
            "Data Structures", "Algorithms", "Database Systems", "Operating Systems",
            "Computer Networks", "Software Engineering", "AI", "Machine Learning",
            "Web Development", "Mobile Computing", "Cloud Computing", "Cybersecurity"
        ]
        
        instructors = ["Dr. Smith", "Dr. Johnson", "Dr. Williams", "Dr. Brown", "Dr. Davis"]
        
        for i in range(min(num_courses, len(course_names))):
            courses.append(Course(
                id=f"CS{101+i}",
                name=course_names[i],
                instructor=instructors[i % len(instructors)],
                duration=3
            ))
        
        # Generate timeslots
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"][:num_days]
        timeslots = []
        for day in days:
            for period in range(1, periods_per_day + 1):
                timeslots.append(TimeSlot(day=day, period=period))
        
        # Generate rooms
        rooms = []
        for i in range(num_rooms):
            room_type = 'lab' if i < num_rooms // 2 else 'classroom'
            rooms.append(Room(
                id=f"R{201+i}",
                capacity=40 + (i * 10),
                type=room_type
            ))
        
        # Instructor constraints (unavailable days) - More restrictive
        instructor_constraints = {
            "Dr. Smith": ["Friday", "Thursday"],
            "Dr. Johnson": ["Wednesday", "Thursday"],
            "Dr. Williams": ["Monday", "Friday"],
            "Dr. Brown": ["Tuesday", "Wednesday"],
            "Dr. Davis": ["Monday", "Wednesday", "Thursday"]
        }
        
        # Conflicting preferences
        # Severely conflicting preferences - forces backtracking
        preferred_times = {
            "CS101": [("Monday", 1)],  # Only 1 option
            "CS102": [("Monday", 1)],  # Same slot as CS101 - CONFLICT
            "CS103": [("Tuesday", 1)],  # Only 1 option
            "CS104": [("Monday", 1)],  # Same slot as CS101, CS102 - CONFLICT
            "CS105": [("Tuesday", 1)],  # Same slot as CS103 - CONFLICT
            "CS106": [("Monday", 2)],  # Only 1 option
            "CS107": [("Monday", 2)],  # Same slot as CS106 - CONFLICT
            "CS108": [("Tuesday", 2)],  # Only 1 option
            "CS109": [("Monday", 2)],  # Same slot as CS106, CS107 - CONFLICT
            "CS110": [("Tuesday", 2)],  # Same slot as CS108 - CONFLICT
        }
        
        return TimetableProblem(courses, timeslots, rooms, instructor_constraints, preferred_times)
    
    @staticmethod
    def generate_complex_problem() -> TimetableProblem:
        """Generate a more complex problem for testing"""
        return TimetableGenerator.generate_sample_problem(
            num_courses=1,
            num_rooms=3,
            num_days=5,
            periods_per_day=8
        )
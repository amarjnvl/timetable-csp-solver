import matplotlib.pyplot as plt
import pandas as pd
from typing import Dict, List, Tuple
from ..models.timetable import Course, TimeSlot, Room
import json
from tabulate import tabulate

class TimetableVisualizer:
    @staticmethod
    def print_timetable(assignment: Dict[Course, Tuple[TimeSlot, Room]]):
        """Print timetable in readable format"""
        if not assignment:
            print("No solution found!")
            return
        
        print("\n" + "="*80)
        print("TIMETABLE SOLUTION".center(80))
        print("="*80 + "\n")
        
        # Group by day
        schedule = {}
        for course, (timeslot, room) in assignment.items():
            day = timeslot.day
            if day not in schedule:
                schedule[day] = []
            schedule[day].append({
                'Period': timeslot.period,
                'Course': f"{course.id} - {course.name}",
                'Instructor': course.instructor,
                'Room': room.id
            })
        
        # Print each day
        for day in sorted(schedule.keys()):
            print(f"\n{day}")
            print("-" * 80)
            day_schedule = sorted(schedule[day], key=lambda x: x['Period'])
            print(tabulate(day_schedule, headers='keys', tablefmt='grid'))
        
        print("\n" + "="*80 + "\n")
    
    @staticmethod
    def save_timetable_to_file(assignment: Dict[Course, Tuple[TimeSlot, Room]], 
                               filename: str):
        """Save timetable to JSON file"""
        data = []
        for course, (timeslot, room) in assignment.items():
            data.append({
                'course_id': course.id,
                'course_name': course.name,
                'instructor': course.instructor,
                'day': timeslot.day,
                'period': timeslot.period,
                'room': room.id
            })
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"Timetable saved to {filename}")
    
    @staticmethod
    def plot_performance_comparison(metrics_list: List[Dict], 
                                   labels: List[str],
                                   output_file: str):
        """Plot performance comparison between methods"""
        
        # Extract metrics
        metrics_data = {
            'nodes_explored': [],
            'backtracks': [],
            'time_taken': [],
            'pruned_values': []
        }
        
        for metrics in metrics_list:
            metrics_data['nodes_explored'].append(metrics.get('nodes_explored', 0))
            metrics_data['backtracks'].append(metrics.get('backtracks', 0))
            metrics_data['time_taken'].append(metrics.get('time_taken', 0))
            metrics_data['pruned_values'].append(metrics.get('pruned_values', 0))
        
        # Create subplots
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('Performance Comparison: Backtracking Methods', fontsize=16, fontweight='bold')
        
        # Plot 1: Nodes Explored
        axes[0, 0].bar(labels, metrics_data['nodes_explored'], color=['#3498db', '#e74c3c'])
        axes[0, 0].set_title('Nodes Explored', fontweight='bold')
        axes[0, 0].set_ylabel('Count')
        axes[0, 0].grid(axis='y', alpha=0.3)
        
        # Plot 2: Backtracks
        axes[0, 1].bar(labels, metrics_data['backtracks'], color=['#2ecc71', '#f39c12'])
        axes[0, 1].set_title('Number of Backtracks', fontweight='bold')
        axes[0, 1].set_ylabel('Count')
        axes[0, 1].grid(axis='y', alpha=0.3)
        
        # Plot 3: Time Taken
        axes[1, 0].bar(labels, metrics_data['time_taken'], color=['#9b59b6', '#1abc9c'])
        axes[1, 0].set_title('Time Taken (seconds)', fontweight='bold')
        axes[1, 0].set_ylabel('Time (s)')
        axes[1, 0].grid(axis='y', alpha=0.3)
        
        # Plot 4: Pruned Values (only for forward checking)
        if any(v > 0 for v in metrics_data['pruned_values']):
            axes[1, 1].bar(labels, metrics_data['pruned_values'], color=['#34495e', '#e67e22'])
            axes[1, 1].set_title('Values Pruned (Forward Checking)', fontweight='bold')
            axes[1, 1].set_ylabel('Count')
            axes[1, 1].grid(axis='y', alpha=0.3)
        else:
            axes[1, 1].text(0.5, 0.5, 'Pruning only in\nForward Checking', 
                          ha='center', va='center', fontsize=12)
            axes[1, 1].set_xticks([])
            axes[1, 1].set_yticks([])
        
        plt.tight_layout()
        plt.savefig(output_file, dpi=300, bbox_inches='tight')
        print(f"Performance graph saved to {output_file}")
        plt.close()
    
    @staticmethod
    def print_metrics_table(metrics_list: List[Dict], labels: List[str]):
        """Print metrics in table format"""
        data = []
        for label, metrics in zip(labels, metrics_list):
            data.append({
                'Method': label,
                'Nodes Explored': metrics.get('nodes_explored', 0),
                'Backtracks': metrics.get('backtracks', 0),
                'Pruned Values': metrics.get('pruned_values', 0),
                'Time (s)': f"{metrics.get('time_taken', 0):.4f}",
                'Success': '✓' if metrics.get('success', False) else '✗'
            })
        
        print("\n" + "="*100)
        print("PERFORMANCE METRICS".center(100))
        print("="*100)
        print(tabulate(data, headers='keys', tablefmt='grid'))
        print("="*100 + "\n")
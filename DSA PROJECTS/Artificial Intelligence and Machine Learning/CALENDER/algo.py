import numpy as np
import random
from datetime import datetime, timedelta

def parse_time(time_str):
    return datetime.strptime(time_str, "%H:%M").time()

def add_time(time_obj, minutes):
    return (datetime.combine(datetime.today(), time_obj) + timedelta(minutes=minutes)).time()

def check_overlap(start, end, intervals):
    for interval in intervals:
        if start < interval[1] and end > interval[0]:
            return True
    return False

# Example fixed events
fixed_events = [
    {"title": "Math Tuition", "start_time": "10:00", "end_time": "12:00"},
    {"title": "Meeting", "start_time": "16:00", "end_time": "18:00"},
    {"title": "Lunch", "start_time": "12:00", "end_time": "12:30"}
]

# Example variable events
variable_events = [
    {"title": "Computing", "weekly_hours": 3},
    {"title": "Chemistry", "weekly_hours": 2}
]

# User-defined goals
study_goals = {
    "Computing": ["Finish chapter 5", "Practice coding"],
    "Chemistry": ["Complete lab report", "Study for test"]
}

# Sleep schedule
sleep_schedule = {"start_time": "23:00", "end_time": "07:00"}

# Define time slots (30 minutes each)
time_slots = [(add_time(parse_time("07:00"), 30 * i), add_time(parse_time("07:00"), 30 * (i + 1))) for i in range(((parse_time("23:00").hour - parse_time("07:00").hour) * 2) + 1)]

# Q-learning parameters
alpha = 0.1
gamma = 0.9
epsilon = 0.1

# Q-table initialization
state_space_size = len(time_slots) * len(variable_events)
q_table = np.zeros((state_space_size, len(variable_events)))

def state_to_index(state):
    time_slot_index, event_index = state
    return time_slot_index * len(variable_events) + event_index

def get_reward(action, state, fixed_intervals, variable_events):
    current_time_slot, event_index = state
    event = variable_events[action]
    study_duration = 30  # 30 minutes slot

    start_time = time_slots[current_time_slot][0]
    end_time = add_time(start_time, study_duration)
    
    if check_overlap(start_time, end_time, fixed_intervals):
        return -1  # Negative reward for conflict
    if event['weekly_hours'] <= 0:
        return -1  # Negative reward for exceeding required study hours

    return 1  # Positive reward for a valid slot

def q_learning_schedule(fixed_events, variable_events, sleep_schedule, study_goals, episodes=1000):
    day_start = parse_time(sleep_schedule["end_time"])
    day_end = parse_time(sleep_schedule["start_time"])
    current_date = datetime.now().date()

    # Process fixed events
    fixed_intervals = []
    for event in fixed_events:
        start = parse_time(event["start_time"])
        end = parse_time(event["end_time"])
        fixed_intervals.append((start, end))

    for episode in range(episodes):
        state = (0, 0)  # Start at the beginning of the day, first variable event
        done = False

        while not done:
            state_index = state_to_index(state)
            if random.uniform(0, 1) < epsilon:
                action = random.randint(0, len(variable_events) - 1)
            else:
                action = np.argmax(q_table[state_index])

            reward = get_reward(action, state, fixed_intervals, variable_events)
            next_state = (state[0] + 1, action) if state[0] < len(time_slots) - 1 else (0, state[1] + 1)
            next_state_index = state_to_index(next_state)
            done = next_state[1] >= len(variable_events)

            q_table[state_index, action] = q_table[state_index, action] + alpha * (reward + gamma * np.max(q_table[next_state_index]) - q_table[state_index, action])
            state = next_state

    weekly_schedule = []

    # Add fixed events to the schedule
    for event in fixed_events:
        weekly_schedule.append({
            "date": current_date,
            "title": event["title"],
            "start_time": parse_time(event["start_time"]),
            "end_time": parse_time(event["end_time"]),
            "goal": event["title"]
        })

    current_time_index = 0
    for event in variable_events:
        total_minutes = event["weekly_hours"] * 60
        while total_minutes > 0 and current_time_index < len(time_slots):
            state_index = state_to_index((current_time_index, variable_events.index(event)))
            best_action = np.argmax(q_table[state_index])
            start_time = time_slots[current_time_index][0]
            end_time = add_time(start_time, 30)
            if not check_overlap(start_time, end_time, fixed_intervals):
                goal_index = (current_time_index // 4) % len(study_goals[event["title"]])
                weekly_schedule.append({
                    "date": current_date,
                    "title": event["title"],
                    "start_time": start_time,
                    "end_time": end_time,
                    "goal": study_goals[event["title"]][goal_index]
                })
                total_minutes -= 30
                fixed_intervals.append((start_time, end_time))  # Add to fixed intervals to prevent overlap
            current_time_index += 1

    return sorted(weekly_schedule, key=lambda x: (x["date"], x["start_time"]))

def save_schedule_to_file(schedule, filename):
    with open(filename, 'w') as f:
        current_date = None
        for session in schedule:
            if session["date"] != current_date:
                current_date = session["date"]
                f.write(f"Date: {current_date}\n")
            start_time = session["start_time"].strftime("%H:%M")
            end_time = session["end_time"].strftime("%H:%M")
            goal = session["goal"]
            f.write(f"  {start_time} - {end_time}: {goal}\n")
        f.write("\n")

# Example usage
weekly_schedule = q_learning_schedule(fixed_events, variable_events, sleep_schedule, study_goals)
save_schedule_to_file(weekly_schedule, "schedule.txt")


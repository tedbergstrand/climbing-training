import time
import os
import json
import threading
import sys


class Exercise:
    def __init__(self, name, exercise_type, energy_system, sets, repetitions, hang_time, short_rest, long_rest, message, user_grade=None, input_prompts=None, short_rest_multiplier=None, long_rest_multiplier=None):
        self.name = name
        self.exercise_type = exercise_type
        self.energy_system = energy_system
        self.sets = sets
        self.repetitions = repetitions
        self.hang_time = hang_time
        self.short_rest = short_rest
        self.long_rest = long_rest
        self.message = message
        self.input_prompts = input_prompts or {}
        self.short_rest_multiplier = short_rest_multiplier
        self.long_rest_multiplier = long_rest_multiplier
        self.user_grade = user_grade

    def get_user_input(self):
        self.user_timed = False  # introduce a flag to check if the user timed the exercise
        for param, prompt in self.input_prompts.items():
            print("\n---\n")
            print(f"Do you want to:\n")
            print(f"1. Use the recommended value / time estimate")
            print(f"2. Input your own value / time estimate")
            print(f"3. Time an actual rep (where applicable)")
            print(f"0. Go back to the previous menu")
            choice = input("\nChoose a number (press Enter for default): ")
            if choice == "1" or choice == "":
                continue
            elif choice == "2":
                user_input = int(input(prompt))
                # Convert the input to seconds if the prompt is asking for minutes
                if "minutes" in prompt:
                    user_input *= 60
                setattr(self, param, user_input)
            elif choice == "3":
                actual_time = self.time_actual_exercise_auto_start()  # modified this to the auto start version
                print(f"\nTime recorded: {actual_time} seconds.")
                setattr(self, param, actual_time)
                self.user_timed = True  # set the flag to True if the user timed the exercise
            elif choice == "0":
                return



    

    def time_actual_exercise_auto_start(self):
        print("\nStarting timer immediately after 'Get Ready' timer beeps... Get ready to start.")
        stop_event_dummy = threading.Event()  # Create a dummy event since you don't intend to stop this timer.
        timer_with_beep(10, f"\nGet Ready for {self.name}", stop_event_dummy)

        start_time = time.time()
        input("\nPerform the exercise... Press Enter to stop timing once done.")
        end_time = time.time()
        return int(end_time - start_time)


    def time_actual_exercise(self):
        input("\nPress Enter to start timing...")
        start_time = time.time()
        input("\nPerform the exercise... Press Enter to stop timing once done.")
        end_time = time.time()
        return int(end_time - start_time)

    def display_description(self, user_grade):
        with open("exercise_descriptions.json", "r") as file:
            descriptions = json.load(file)
            if self.name in descriptions:
                print(f"\nExercise: {self.name}\n")
                for key, value in descriptions[self.name].items():
                    if isinstance(value, dict):
                        print("\n" + key + ":")
                        for sub_key, sub_value in value.items():
                            print(f"\n  - {sub_key}: {sub_value}")
                    else:
                        print(f"\n{key}: {value}")
            else:
                print("\nNo description available for this exercise.")
            recommended = recommended_grade(self.user_grade, self.name)
            print(f"\nRecommended Grade: V{recommended}")
            print("\n---\n")
            input("Press Enter when you understand the exercise...\n")

    def run(self):
        self.display_description(self.user_grade)
        self.get_user_input()

        # Adjust the short_rest if short_rest_multiplier is provided
        actual_short_rest = self.short_rest
        if self.short_rest_multiplier:
            actual_short_rest = int(self.hang_time * self.short_rest_multiplier)

        # Adjust the long_rest if long_rest_multiplier is provided
        actual_long_rest = self.long_rest
        if self.long_rest_multiplier:
            actual_long_rest = int(self.hang_time * self.long_rest_multiplier)

        # Only start the "Get Ready" timer if the user hasn't timed an actual rep
        if not self.user_timed:
            print("\n---")
            stop_event_dummy = threading.Event()  # Create a dummy event since you don't intend to stop this timer.
            timer_with_beep(10, f"\nGet Ready for {self.name}", stop_event_dummy)


        stop_event = threading.Event()  # Create an event to signal stopping

        is_first_set = True
        for _ in range(self.sets):
            start_rep = 1 if self.user_timed and is_first_set else 0
            if start_rep == 1:
                print("\nSkipping the first repetition since you already performed it.")
                if actual_short_rest:
                    timing_thread = threading.Thread(target=timer_with_beep, args=(actual_short_rest, "Short rest", stop_event))
                    input_thread = threading.Thread(target=listen_for_stop, args=(stop_event,))
                    timing_thread.start()
                    input_thread.start()
                    timing_thread.join()
                    input_thread.join(timeout=0.1)
                    if stop_event.is_set():
                        return

                is_first_set = False
            for rep in range(start_rep, self.repetitions):
                timing_thread = threading.Thread(target=timer_with_beep, args=(self.hang_time, self.message, stop_event))
                input_thread = threading.Thread(target=listen_for_stop, args=(stop_event,))
                timing_thread.start()
                input_thread.start()
                timing_thread.join()
                input_thread.join(timeout=0.1)
                if stop_event.is_set():
                    return
                if actual_short_rest:
                    timing_thread = threading.Thread(target=timer_with_beep, args=(actual_short_rest, "Short rest", stop_event))
                    input_thread = threading.Thread(target=listen_for_stop, args=(stop_event,))
                    timing_thread.start()
                    input_thread.start()
                    timing_thread.join()
                    input_thread.join(timeout=0.1)
                    if stop_event.is_set():
                        return
            if actual_long_rest:
                timing_thread = threading.Thread(target=timer_with_beep, args=(actual_long_rest, "Rest between sets", stop_event))
                input_thread = threading.Thread(target=listen_for_stop, args=(stop_event,))
                timing_thread.start()
                input_thread.start()
                timing_thread.join()
                input_thread.join(timeout=0.1)
                if stop_event.is_set():
                    return









class ExerciseManager:
    def __init__(self):
        self.exercises = []
    
    def add_exercise(self, exercise):
        self.exercises.append(exercise)
        
    ENERGY_SYSTEM_ORDER = ["Aerobic Capacity", "Anaerobic Capacity", "Aerobic Power", "Anaerobic Power"]

    def list_energy_systems_by_type(self, exercise_type):
        energy_systems = set([e.energy_system for e in self.exercises if e.exercise_type == exercise_type])
        sorted_energy_systems = sorted(energy_systems, key=self.ENERGY_SYSTEM_ORDER.index)
        print("\n---\n")
        print("Choose an energy system component\n")
        for idx, energy_system in enumerate(sorted_energy_systems, 1):
            print(f"{idx}. {energy_system}")
        return sorted_energy_systems
    
    def list_exercises_by_type_and_energy(self, exercise_type, energy_system):
        if exercise_type == "on-the-wall":
            exercises_to_list = [e for e in self.exercises if e.exercise_type == exercise_type and e.energy_system == energy_system]
        else:
            exercises_to_list = [e for e in self.exercises if e.exercise_type == exercise_type]
        print("\n---\n")
        print(f"{energy_system}\n")
        for idx, exercise in enumerate(exercises_to_list, 1):
            print(f"{idx}. {exercise.name}")

    def run_exercise_by_type_and_energy(self, exercise_type, user_grade):
        if exercise_type == "on-the-wall":
            energy_systems = self.list_energy_systems_by_type(exercise_type)
            choice = input("\nChoose an energy system by number (or 0 to go back): ")
            
            if choice == "0":
                return
            
            if 1 <= int(choice) <= len(energy_systems):
                selected_energy_system = energy_systems[int(choice)-1]
            else:
                print("\nInvalid choice. Please select a valid energy system number.")
                return
        else:
            selected_energy_system = None  # For other exercise types, energy system is not relevant

        self.list_exercises_by_type_and_energy(exercise_type, selected_energy_system)
        exercise_choice = input("\nChoose an exercise by number (or 0 to go back): ")
        
        if exercise_choice == "0":
            return

        exercises_of_type_and_energy = [e for e in self.exercises if e.exercise_type == exercise_type and (selected_energy_system is None or e.energy_system == selected_energy_system)]
        
        if 1 <= int(exercise_choice) <= len(exercises_of_type_and_energy):
            exercises_of_type_and_energy[int(exercise_choice)-1].run()
        else:
            print("\nInvalid choice. Please select a valid exercise number.")

def listen_for_stop(stop_event):
    input("\n\n---\nPress Enter to stop the exercise and return to the menu...\n")
    stop_event.set()  # Send a stop signal

def timer_with_beep(duration, message, stop_event):
    for i in range(duration, 0, -1):
        if stop_event.is_set():  # Check if the stop signal is set
            break
        print(f"\n{message} - Time left: {i} seconds")
        time.sleep(1)
    beep()
    print("\n---\n")

def beep():
    duration = .5  # duration in seconds
    freq = 440  # frequency in Hz
    print("\n---\n\nBeep\n")  # This might produce a beep sound in some terminals.
    os.system(f'play -nq -t alsa synth {duration} sine {freq}')

def recommended_grade(user_grade, exercise):
    grade_diff = {
        'Continuous Climbing (ARC Training)': -3,
        'Moderate Intensity Climbing': -2,
        'Up-Down Climbing': -2,
        'Circuits': -1,
        'On-The-Minute Climbs': -1,
        '4x4s': -1,
        'Long Boulders': .5,
        'Power Intervals': .5,
        'Climbing Bursts': .5,
        'Maximal Intensity Climbs': 1,
        'Dynamic Movements': 2,
        'Limit Bouldering': 2
    }
    # Check if the exercise is in the grade_diff dictionary
    if exercise in grade_diff:
        return user_grade + grade_diff[exercise]
    else:
        return None

def get_user_grade():
    while True:
        grade_input = input("Enter your comfortable flash grade: V ").lower()
        try:
            # Extract the grade number
            grade = int("".join(filter(str.isdigit, grade_input)))
            return grade
        except ValueError:
            print("Invalid grade. Please enter in the form of v*, V*, or simply *.")


def main():
    manager = ExerciseManager()

    user_grade = get_user_grade()

    # Fingerboard Aerobic Repeaters
    manager.add_exercise(Exercise(
        name="Fingerboard Aerobic Repeaters",
        exercise_type="hangboard",
        energy_system="Aerobic Capacity",
        sets=8,
        repetitions=1,
        hang_time=30,
        short_rest=0,
        long_rest=30,
        message="Hang from the fingerboard for Aerobic Repeaters"
    ))

    # Fingerboard Repeaters
    manager.add_exercise(Exercise(
        name="Fingerboard Repeaters",
        exercise_type="hangboard",
        energy_system="Anaerobic Capacity",
        sets=5,
        repetitions=6,
        hang_time=7,
        short_rest=3,
        long_rest=180,
        message="Hang from the fingerboard for Repeaters"
    ))

    # Fingerboard Capacity Max Hangs
    manager.add_exercise(Exercise(
        name="Fingerboard Capacity Max Hangs",
        exercise_type="hangboard",
        energy_system="Anaerobic Capacity",
        sets=5,
        repetitions=1,
        hang_time=20,
        short_rest=0,
        long_rest=180,
        message="Hang from the fingerboard for Capacity Max Hangs"
    ))

    # Fingerboard Max Hangs
    manager.add_exercise(Exercise(
        name="Fingerboard Max Hangs",
        exercise_type="hangboard",
        energy_system="Anaerobic Power",
        sets=5,
        repetitions=1,
        hang_time=10,
        short_rest=0,
        long_rest=180,
        message="Hang from the fingerboard"
    ))

    
    manager.add_exercise(Exercise(
        name="On-The-Minute Climbs",
        exercise_type="on-the-wall",
        energy_system="Aerobic Power",
        sets=1,
        repetitions=8,
        hang_time=60,
        short_rest=0,
        long_rest=0,
        user_grade=user_grade,
        message="Complete the boulder and rest until the next beep",
        input_prompts={
            'repetitions': 'How many reps would you like to do? '
        }
    ))

        # Up-Down Climbing
    manager.add_exercise(Exercise(
        name="Up-Down Climbing",
        exercise_type="on-the-wall",
        energy_system="Aerobic Capacity",
        sets=1,
        repetitions=1,
        hang_time=15*60,
        short_rest=0,
        long_rest=0,
        user_grade=user_grade,
        message="Climb up and down without resting",
        input_prompts={
            'sets': 'How many sets would you like to do? '
        }
    ))

    # Climbing Bursts
    manager.add_exercise(Exercise(
        name="Climbing Bursts",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Capacity",
        sets=6,
        repetitions=1,
        hang_time=20,
        short_rest=0,
        long_rest=180,
        user_grade=user_grade,
        message="Perform explosive climbing moves"
    ))




    # Limit Bouldering
    # Note: The duration is fetched using the get_climb_duration function. 
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time.
    manager.add_exercise(Exercise(
        name="Limit Bouldering",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Power",
        sets=4,
        repetitions=4,
        hang_time=15,  # This will be overridden by user input
        short_rest=15,
        long_rest=600,
        user_grade=user_grade,
        short_rest_multiplier=1,
        message="Attempt the hardest moves or sequences",
        input_prompts={
            'hang_time': 'How long do you want to attempt the hardest moves or sequences? (in seconds) '
        }
    ))


    manager.add_exercise(Exercise(
        name="Maximal Intensity Climbs",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Power",
        sets=6,
        repetitions=1,
        hang_time=15,  # This is an average between 10-15 seconds
        short_rest=0,
        long_rest=600,  # Rest for 10 minutes
        user_grade=user_grade,
        message="Attempt short sequences with maximal effort moves. Push your limits!",
        input_prompts={
            'hang_time': 'How many seconds does your attempt take? '
        }
    ))

    manager.add_exercise(Exercise(
        name="Dynamic Movements",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Power",
        sets=6,
        repetitions=1,
        hang_time=12,  # This is an average between 5-10 seconds
        short_rest=0,
        long_rest=180,  # This is an average between 2-3 minutes
        user_grade=user_grade,
        message="Focus on power development through dynamic, explosive movements.",
        input_prompts={
            'hang_time': 'How many seconds does your sequence take? '
        }
    ))

    # "Continuous Climbing (ARC Training)" Exercise
    # Note: The user would typically be prompted for the duration.
    # I've kept a placeholder for now for simplicity.
    manager.add_exercise(Exercise(
        name="Continuous Climbing (ARC Training)",
        exercise_type="on-the-wall",
        energy_system="Aerobic Capacity",
        sets=3,
        repetitions=1,
        hang_time=20*60,  # Placeholder for 20 minutes. Replace with user input.
        short_rest=0,
        long_rest=600,
        user_grade=user_grade,
        message="Climb at a constant intensity",
        input_prompts={
            'hang_time': 'How many minutes do you want to stay on the wall? '
        }
    ))

    # "Moderate Intensity Climbing" Exercise
    # Note: The user would typically be prompted for the duration.
    # I've kept a placeholder for now for simplicity.
    manager.add_exercise(Exercise(
        name="Moderate Intensity Climbing",
        exercise_type="on-the-wall",
        energy_system="Aerobic Capacity",
        sets=1,
        repetitions=1,
        hang_time=10*60,  # Placeholder for 10 minutes. Replace with user input.
        short_rest=0,
        long_rest=0,
        user_grade=user_grade,
        message="Climb at a moderate intensity"
    ))

    # "Circuits" Exercise
    # Note: The climb duration is fetched using the get_climb_duration function.
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time before adding the exercise.
    manager.add_exercise(Exercise(
        name="Circuits",
        exercise_type="on-the-wall",
        energy_system="Aerobic Power",
        sets=3,  # Placeholder for 3 sets. Replace with user input.
        repetitions=1,
        hang_time=90,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=180,  # Placeholder for rest being double the climb time. Adjust as needed.
        message="Climb the circuit",
        short_rest_multiplier=2,
        user_grade=user_grade,
        input_prompts={
            'hang_time': 'How many seconds does your circuit take? '
        }
    ))

    # "4x4s" Exercise
    # Note: The climb duration is fetched using the get_climb_duration function.
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time before adding the exercise.
    manager.add_exercise(Exercise(
        name="4x4s",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Capacity",
        sets=4,  # Always 4 rounds for 4x4s
        repetitions=1,  # 1 rep is all 4 boulders
        hang_time=110,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=240,  # Rest between rounds
        long_rest_multiplier=3,
        user_grade=user_grade,
        message="Climb the boulder problem",
        input_prompts={
            'hang_time': 'How many seconds does it take do all 4 problems? '
        }
    ))

    # "Long Boulders" Exercise
    # Note: The climb duration is fetched using the get_climb_duration function.
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time before adding the exercise.
    manager.add_exercise(Exercise(
        name="Long Boulders",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Capacity",
        sets=1,  # Placeholder for 8 sets. Replace with user input.
        repetitions=8,
        hang_time=30,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=60,  # Placeholder for rest being double the climb time. Adjust as needed.
        long_rest_multiplier=3,
        user_grade=user_grade,
        message="Climb the boulder problem or circuit",
        input_prompts={
            'hang_time': 'How many seconds does it take climb your problem? '
        }
    ))

    # "Power Intervals" Exercise
    manager.add_exercise(Exercise(
        name="Power Intervals",
        exercise_type="on-the-wall",
        energy_system="Anaerobic Capacity",
        sets=8,  # Placeholder for 8 sets. Replace with user input.
        repetitions=1,
        hang_time=35,  # Climb duration of 35 seconds
        short_rest=0,
        long_rest=60,  # Rest for 1 minute
        user_grade=user_grade,
        message="Climb the boulder problem"
    ))

    ##Traditional Exercises

        # Tabata
    manager.add_exercise(Exercise(
        name="Tabata",
        exercise_type="traditional",
        energy_system="Anaerobic Capacity",
        sets=12,
        repetitions=1,
        hang_time=20,
        short_rest=10,
        long_rest=0,
        message="Perform at high intensity!"
    ))

    # Standard HIIT
    manager.add_exercise(Exercise(
        name="Standard HIIT",
        exercise_type="traditional",
        energy_system="Anaerobic Power",
        sets=8,
        repetitions=1,
        hang_time=30,
        short_rest=30,
        long_rest=0,
        message="Perform at high intensity!"
    ))

    # EMOM
    manager.add_exercise(Exercise(
        name="EMOM",
        exercise_type="traditional",
        energy_system="Aerobic Power",
        sets=1,  # 10 minutes as an example
        repetitions=0,
        hang_time=60,  # Full minute
        short_rest=0,
        long_rest=0,
        message="Complete the exercise at the start of the minute and rest until the next beep",
        input_prompts={
            'reps': 'How many reps would you like to do? '
        }
    ))

    # AMRAP (10 minutes in this example)
    manager.add_exercise(Exercise(
        name="10-min AMRAP",
        exercise_type="traditional",
        energy_system="Aerobic Capacity",
        sets=1,
        repetitions=1,
        hang_time=10*60,
        short_rest=0,
        long_rest=0,
        message="Perform as many rounds as possible in 10 minutes!"
    ))

        # Ted's Intervals
    manager.add_exercise(Exercise(
        name="Ted's Intervals",
        exercise_type="traditional",
        energy_system="Aerobic Power",
        sets=4,
        repetitions=4,
        hang_time=20,
        short_rest=0,
        long_rest=0,
        message="Aim for quality over quanitity"
    ))




    # ... add other exercises ...

    while True:
        print("\nExercise Categories:\n")
        print("1. On-The-Wall")
        print("2. Hangboard")
        print("3. Traditional")
        print("4. Exit")
        category_choice = input("\nChoose a category: ")

        if category_choice == "1":
            manager.run_exercise_by_type_and_energy("on-the-wall", user_grade)
        elif category_choice == "2":
            manager.run_exercise_by_type_and_energy("hangboard", user_grade)
        elif category_choice == "3":
            manager.run_exercise_by_type_and_energy("traditional", user_grade)
        elif category_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

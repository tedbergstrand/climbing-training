import time
import os
import json

class Exercise:
    def __init__(self, name, exercise_type, energy_system, sets, repetitions, hang_time, short_rest, long_rest, message, input_prompts=None, short_rest_multiplier=None, long_rest_multiplier=None):
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

    def get_user_input(self):
        self.user_timed = False  # introduce a flag to check if the user timed the exercise
        for param, prompt in self.input_prompts.items():
            print(f"Do you want to:")
            print(f"1. Use the recommended value / time estimate")
            print(f"2. Input your own value / time estimate")
            print(f"3. Time an actual rep (where applicable)")
            choice = input("Choose an option (1, 2, or 3): ")
            if choice == "1":
                continue
            elif choice == "2":
                user_input = int(input(prompt))
                # Convert the input to seconds if the prompt is asking for minutes
                if "minutes" in prompt:
                    user_input *= 60
                setattr(self, param, user_input)
            elif choice == "3":
                actual_time = self.time_actual_exercise_auto_start()  # modified this to the auto start version
                print(f"Time recorded: {actual_time} seconds.")
                setattr(self, param, actual_time)
                self.user_timed = True  # set the flag to True if the user timed the exercise


    

    def time_actual_exercise_auto_start(self):
        print("Starting timer immediately after 'Get Ready' timer... Get ready to start.")
        start_time = time.time()
        input("Perform the exercise... Press Enter to stop timing once done.")
        end_time = time.time()
        return int(end_time - start_time)

    def time_actual_exercise(self):
        input("Press Enter to start timing...")
        start_time = time.time()
        input("Perform the exercise... Press Enter to stop timing once done.")
        end_time = time.time()
        return int(end_time - start_time)

    def display_description(self):
        with open("exercise_descriptions.json", "r") as file:
            descriptions = json.load(file)
            if self.name in descriptions:
                print(f"\nExercise: {self.name}\n")
                for key, value in descriptions[self.name].items():
                    if isinstance(value, dict):
                        print(key + ":")
                        for sub_key, sub_value in value.items():
                            print(f"  - {sub_key}: {sub_value}")
                    else:
                        print(f"{key}: {value}")
                print("\n")
            else:
                print("No description available for this exercise.\n")
            input("Press Enter when you're ready to continue...\n")

    def run(self):
        self.display_description()
        self.get_user_input()

        # Adjust the short_rest if short_rest_multiplier is provided
        actual_short_rest = self.short_rest
        if self.short_rest_multiplier:
            actual_short_rest = int(self.hang_time * self.short_rest_multiplier)
        
        # Adjust the long_rest if long_rest_multiplier is provided
        actual_long_rest = self.long_rest
        if self.long_rest_multiplier:
            actual_long_rest = int(self.hang_time * self.long_rest_multiplier)  # Adjusting long_rest based on multiplier

        timer_with_beep(10, f"Get Ready for {self.name}")
        is_first_set = True
        for _ in range(self.sets):
            start_rep = 1 if self.user_timed and is_first_set else 0
            if start_rep == 1:
                print("Skipping the first repetition since you already performed it.")
                if actual_short_rest:
                    timer_with_beep(actual_short_rest, "Short rest")
                is_first_set = False
            for rep in range(start_rep, self.repetitions):
                timer_with_beep(self.hang_time, self.message)
                if actual_short_rest:
                    timer_with_beep(actual_short_rest, "Short rest")
            if actual_long_rest:
                timer_with_beep(actual_long_rest, "Rest between sets")  # Using the adjusted long rest






class ExerciseManager:
    def __init__(self):
        self.exercises = []
    
    def add_exercise(self, exercise):
        self.exercises.append(exercise)
        
    ENERGY_SYSTEM_ORDER = ["aerobic capacity", "anaerobic capacity", "aerobic power", "anaerobic power"]

    def list_energy_systems_by_type(self, exercise_type):
        energy_systems = set([e.energy_system for e in self.exercises if e.exercise_type == exercise_type])
        sorted_energy_systems = sorted(energy_systems, key=self.ENERGY_SYSTEM_ORDER.index)
        for idx, energy_system in enumerate(sorted_energy_systems, 1):
            print(f"{idx}. {energy_system}")
        return sorted_energy_systems
    
    def list_exercises_by_type_and_energy(self, exercise_type, energy_system):
        if exercise_type == "on-the-wall":
            exercises_to_list = [e for e in self.exercises if e.exercise_type == exercise_type and e.energy_system == energy_system]
        else:
            exercises_to_list = [e for e in self.exercises if e.exercise_type == exercise_type]
        
        for idx, exercise in enumerate(exercises_to_list, 1):
            print(f"{idx}. {exercise.name}")

    def run_exercise_by_type_and_energy(self, exercise_type, user_grade):
        if exercise_type == "on-the-wall":
            energy_systems = self.list_energy_systems_by_type(exercise_type)
            choice = int(input("Choose an energy system by number: "))
            if 1 <= choice <= len(energy_systems):
                selected_energy_system = energy_systems[choice-1]
            else:
                print("Invalid choice. Please select a valid energy system number.")
                return
        else:
            selected_energy_system = None  # For other exercise types, energy system is not relevant

        self.list_exercises_by_type_and_energy(exercise_type, selected_energy_system)
        exercise_choice = int(input("Choose an exercise by number: "))
        exercises_of_type_and_energy = [e for e in self.exercises if e.exercise_type == exercise_type and (selected_energy_system is None or e.energy_system == selected_energy_system)]
        
        if 1 <= exercise_choice <= len(exercises_of_type_and_energy):
            recommended = recommended_grade(user_grade, exercises_of_type_and_energy[exercise_choice-1].name)
            print(f"Recommended bouldering grade for this exercise: V{recommended}")
            exercises_of_type_and_energy[exercise_choice-1].run()
        else:
            print("Invalid choice. Please select a valid exercise number.")

def timer_with_beep(duration, message):
    for i in range(duration, 0, -1):
        print(f"{message} - Time left: {i} seconds")
        time.sleep(1)
    beep()
    print(f"{message} is done!")

def beep():
    duration = .5  # duration in seconds
    freq = 440  # frequency in Hz
    print("Beep")  # This might produce a beep sound in some terminals.
    os.system(f'play -nq -t alsa synth {duration} sine {freq}')

def recommended_grade(user_grade, exercise):
    grade_diff = {
        'Continuous Climbing (ARC Training)': -3,
        'Moderate Intensity Climbing': -2,
        'Up-Down Climbing': -2,
        'Circuits': -1,
        'On-the-Minute': -1,
        '4x4s': -1,
        'Long Boulders': .5,
        'Power Intervals': .5,
        'Climbing Bursts': .5,
        'Maximal Intensity Climbs': 1.5,
        'Dynamic Movements': 1.5,
        'Limit Bouldering': 2
    }
    # Check if the exercise is in the grade_diff dictionary
    if exercise in grade_diff:
        return user_grade + grade_diff[exercise]
    else:
        return None

def get_user_grade():
    while True:
        grade_input = input("Enter your comfortable bouldering grade (e.g. v5, V5, 5): ").lower()
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
        energy_system="aerobic capacity",
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
        energy_system="anaerobic capacity",
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
        energy_system="anaerobic capacity",
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
        energy_system="anaerobic power",
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
        energy_system="aerobic power",
        sets=8,
        repetitions=1,
        hang_time=60,
        short_rest=0,
        long_rest=0,
        message="Complete the boulder and rest until the next beep",
        input_prompts={
            'sets': 'How many reps would you like to do? '
        }
    ))

        # Up-Down Climbing
    manager.add_exercise(Exercise(
        name="Up-Down Climbing",
        exercise_type="on-the-wall",
        energy_system="aerobic capacity",
        sets=1,
        repetitions=1,
        hang_time=15*60,
        short_rest=0,
        long_rest=0,
        message="Climb up and down without resting",
        input_prompts={
            'sets': 'How many sets would you like to do? '
        }
    ))

    # Climbing Bursts
    manager.add_exercise(Exercise(
        name="Climbing Bursts",
        exercise_type="on-the-wall",
        energy_system="anaerobic capacity",
        sets=6,
        repetitions=1,
        hang_time=20,
        short_rest=0,
        long_rest=180,
        message="Perform explosive climbing moves"
    ))




    # Limit Bouldering
    # Note: The duration is fetched using the get_climb_duration function. 
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time.
    manager.add_exercise(Exercise(
        name="Limit Bouldering",
        exercise_type="on-the-wall",
        energy_system="anaerobic power",
        sets=5,
        repetitions=1,
        hang_time=0,  # This will be overridden by user input
        short_rest=0,
        long_rest=300,
        message="Attempt the hardest moves or sequences",
        input_prompts={
            'hang_time': 'How long do you want to attempt the hardest moves or sequences? (in seconds) '
        }
    ))


    manager.add_exercise(Exercise(
        name="Maximal Intensity Climbs",
        exercise_type="on-the-wall",
        energy_system="anaerobic power",
        sets=6,
        repetitions=1,
        hang_time=15,  # This is an average between 10-15 seconds
        short_rest=0,
        long_rest=600,  # Rest for 10 minutes
        message="Attempt short sequences with maximal effort moves. Push your limits!",
        input_prompts={
            'hang_time': 'How many seconds does your attempt take? '
        }
    ))

    manager.add_exercise(Exercise(
        name="Dynamic Movements",
        exercise_type="on-the-wall",
        energy_system="anaerobic power",
        sets=6,
        repetitions=1,
        hang_time=10,  # This is an average between 5-10 seconds
        short_rest=0,
        long_rest=180,  # This is an average between 2-3 minutes
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
        energy_system="aerobic capacity",
        sets=3,
        repetitions=1,
        hang_time=20*60,  # Placeholder for 20 minutes. Replace with user input.
        short_rest=0,
        long_rest=600,
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
        energy_system="aerobic capacity",
        sets=1,
        repetitions=1,
        hang_time=10*60,  # Placeholder for 10 minutes. Replace with user input.
        short_rest=0,
        long_rest=0,
        message="Climb at a moderate intensity"
    ))

    # "Circuits" Exercise
    # Note: The climb duration is fetched using the get_climb_duration function.
    # For simplicity, I'm using a static time for now. 
    # In a real application, you'd prompt the user for this time before adding the exercise.
    manager.add_exercise(Exercise(
        name="Circuits",
        exercise_type="on-the-wall",
        energy_system="aerobic power",
        sets=3,  # Placeholder for 3 sets. Replace with user input.
        repetitions=1,
        hang_time=90,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=180,  # Placeholder for rest being double the climb time. Adjust as needed.
        message="Climb the circuit",
        short_rest_multiplier=2,
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
        energy_system="anaerobic capacity",
        sets=4,  # Always 4 rounds for 4x4s
        repetitions=1,  # 1 rep is all 4 boulders
        hang_time=110,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=240,  # Rest between rounds
        long_rest_multiplier=3,
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
        energy_system="anaerobic capacity",
        sets=1,  # Placeholder for 8 sets. Replace with user input.
        repetitions=8,
        hang_time=30,  # This is a placeholder. Replace with `get_climb_duration()`
        short_rest=0,
        long_rest=60,  # Placeholder for rest being double the climb time. Adjust as needed.
        long_rest_multiplier=3,
        message="Climb the boulder problem or circuit",
        input_prompts={
            'hang_time': 'How many seconds does it take climb your problem? '
        }
    ))

    # "Power Intervals" Exercise
    manager.add_exercise(Exercise(
        name="Power Intervals",
        exercise_type="on-the-wall",
        energy_system="anaerobic capacity",
        sets=8,  # Placeholder for 8 sets. Replace with user input.
        repetitions=1,
        hang_time=35,  # Climb duration of 35 seconds
        short_rest=0,
        long_rest=60,  # Rest for 1 minute
        message="Climb the boulder problem"
    ))




    # ... add other exercises ...

    while True:
        print("\nExercise Categories:")
        print("1. Hangboard")
        print("2. On-The-Wall")
        print("3. Traditional")
        print("4. Exit")
        category_choice = input("Choose a category: ")

        if category_choice == "1":
            manager.run_exercise_by_type_and_energy("hangboard", user_grade)
        elif category_choice == "2":
            manager.run_exercise_by_type_and_energy("on-the-wall", user_grade)
        elif category_choice == "3":
            manager.run_exercise_by_type_and_energy("traditional", user_grade)
        elif category_choice == "4":
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
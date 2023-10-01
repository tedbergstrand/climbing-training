import time
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load the beep sound from the same directory as the script
beep_sound = pygame.mixer.Sound('beep-07.wav')

def beep():
    """Play beep sound using pygame."""
    beep_sound.play()

def timer_with_beep(duration, message):
    for i in range(duration, 0, -1):
        print(f"{message} - Time left: {i} seconds")
        time.sleep(1)
    beep()
    print(f"{message} is done!")

import time

def get_climb_duration():
    choice = input("Do you want to enter an estimated climb time or press a key after you finish climbing? (Enter '1' for estimate or '2' for keypress): ")
    
    if choice == '1':
        return int(input("Enter your estimated climb time in seconds: "))
    elif choice == '2':
        input("\nGet to the problem and back very quickly. Do not waste time. \n\nPress Enter to start climbing and press it again when you finish.")
        start_time = time.time()
        input("\nPress Enter now that you've finished your climb.")
        end_time = time.time()
        return int(end_time - start_time)
    else:
        print("Invalid choice. Defaulting to keypress method.")
        return get_climb_duration()


def recommended_grade(user_grade, exercise):
    grade_diff = {
        'Continuous Climbing (ARC Training)': -3,
        'Moderate Intensity Climbing': -2,
        'Up-Down Climbing': -2,
        'Circuits': -1,
        'On-the-Minute': -1,
        '4x4s (Boulder Edition)': -1,
        'Long Boulders': .5,
        'Power Intervals': .5,
        'Climbing Bursts': .5,
        'Maximal Intensity Climbs': 1.5,
        'Dynamic Movements': 1.5,
        'Limit Bouldering': 2
    }
    return user_grade + grade_diff[exercise]

def fingerboard_max_hangs():
    sets = int(input("How many sets do you want to perform for Max Hangs (e.g., 5)? "))
    hang_time = 10  # 10 seconds
    rest_time = 180  # 3 minutes in seconds

    timer_with_beep(10, "Get Ready for Max Hangs")
    for _ in range(sets):
        timer_with_beep(hang_time, "Hang from the fingerboard")
        timer_with_beep(rest_time, "Rest")

def fingerboard_repeaters():
    sets = int(input("How many sets do you want to perform for Repeaters (e.g., 5)? "))
    repetitions = 6
    hang_time = 7  # 7 seconds
    short_rest = 3  # 3 seconds
    long_rest = 180  # 3 minutes in seconds
    timer_with_beep(10, "Get Ready for Repeaters")

    for _ in range(sets):
        for _ in range(repetitions):
            timer_with_beep(hang_time, "Hang from the fingerboard")
            timer_with_beep(short_rest, "Short rest")
        timer_with_beep(long_rest, "Rest between sets")

def fingerboard_power_repeaters():
    sets = int(input("How many sets do you want to perform for Power Repeaters (e.g., 6)? "))
    repetitions = 5  # 5-6 hangs per set
    hang_time = 10  # 10 seconds
    short_rest = 5  # 5 seconds
    long_rest = 180  # 3 minutes in seconds

    timer_with_beep(10, "Get Ready for Power Repeaters")
    for _ in range(sets):
        for _ in range(repetitions):
            timer_with_beep(hang_time, "Hang from the fingerboard")
            timer_with_beep(short_rest, "Short rest")
        timer_with_beep(long_rest, "Rest between sets")

def fingerboard_capacity_max_hangs():
    sets = int(input("How many sets do you want to perform for Capacity Max Hangs (e.g., 5)? "))
    hang_time = 20  # 20 seconds
    rest_time = 120  # 2 minutes in seconds

    timer_with_beep(10, "Get Ready for Capacity Max Hangs")
    for _ in range(sets):
        timer_with_beep(hang_time, "Hang from the fingerboard")
        timer_with_beep(rest_time, "Rest")

def fingerboard_power_max_hangs():
    sets = int(input("How many sets do you want to perform for Power Max Hangs (e.g., 5)? "))
    hang_time = 5  # 5 seconds
    rest_time = 180  # 3 minutes in seconds

    timer_with_beep(10, "Get Ready for Power Max Hangs")
    for _ in range(sets):
        timer_with_beep(hang_time, "Hang from the fingerboard")
        timer_with_beep(rest_time, "Rest")


def fingerboard_aerobic_repeaters():
    sets = int(input("How many sets do you want to perform for Aerobic Repeaters (e.g., 4)? "))
    hang_time = 30  # 30 seconds
    rest_time = 30  # 30 seconds

    timer_with_beep(10, "Get Ready for Aerobic Repeaters")
    for _ in range(sets):
        timer_with_beep(hang_time, "Hang from the fingerboard")
        timer_with_beep(rest_time, "Rest")


def choose_exercise(component):
    exercises = {
    'Aerobic Capacity': [
        '''
Exercise: Continuous Climbing (ARC Training)

Objective: Improve aerobic capacity by climbing continuously at a low intensity.
Climbing Details:
- Duration: 20-40 minutes
- Intensity: Low, constant
- Mode: Routes or traversing on an empty bouldering wall.
- Falls: If you fall, get back on the wall quickly to maintain continuous climbing.
- Cruxes: Avoid cruxes or highly challenging moves. The focus is on endurance, not overcoming hard moves.
Rest Details: None. The goal is to keep climbing without resting.
Repetitions: 1 (This is a continuous exercise)
Intensity: This should feel relatively easy, around 4-5 out of 10.
        ''',
        '''
Exercise: Moderate Intensity Climbing

Objective: Build basic endurance through sustained climbing at a moderate intensity.
Climbing Details:
- Duration: 10 minutes
- Intensity: Moderate
- Mode: Climb routes or boulder problems that offer a steady challenge.
- Falls: If you fall, take a brief moment to shake out and then continue.
- Cruxes: It's okay to face cruxes, but they shouldn't stop your progress for long. Adjust your route choice if needed.
Rest Details: None. Try to climb the full duration.
Repetitions: 1
Intensity: Around 6 out of 10. You should feel worked, but not to exhaustion.
        ''',
        '''
Exercise: Up-Down Climbing

Objective: Develop and maintain a steady aerobic pace while enhancing mental endurance and route reading on familiar terrain.
Climbing Details:
- Duration: 15 minutes
- Intensity: Low to moderate
- Mode: Choose a boulder or route you're familiar with. Climb it upwards, then try to reverse the movements to climb downwards. Repeat for 15 minutes without getting off the wall.
- Falls: If you fall, take a short break, then continue where you left off.
- Cruxes: Opt for problems or routes with minimal cruxes to maintain a steady flow.
Rest Details: None during the exercise. Keep climbing up and down.
Repetitions: 1
        '''
    ],
    'Aerobic Power': [
        '''
Exercise: Circuits

Objective: Enhance aerobic power by simulating long sequences commonly found outdoors.
Climbing Details:
- Duration: Duration depends on the circuit complexity.
- Move Count: 30 moves
- Intensity: High
- Mode: Set a circuit that simulates the sequence and style of an outdoor climb. No resting holds allowed.
- Falls: If you fall, get back on immediately and continue.
Rest Details: Rest 1-2 times the duration of your climb.
Repetitions: Varies. 8 reps for an intense session or 6 sets of 4 reps with 10-20min rests between for a high-volume session.
Intensity: Should feel hard by the last few reps, potentially leading to failure.
        ''',
        '''
Exercise: On-the-Minute

Objective: Increase aerobic power by maintaining a consistent climb-to-rest ratio.
Climbing Details:
- Duration: Depends on the boulder problem but should fit within the 60-second timeframe.
- Move Count: 6-8 moves
- Intensity: High
- Mode: Bouldering. Start a new climb every minute.
- Falls: Get back on immediately if you fall. The goal is to maintain the rhythm.
Rest Details: Rest for the remainder of the minute (usually 40 seconds if the climb takes 20 seconds).
Repetitions: 8 reps per set, adjust the number of sets based on desired volume.
        ''',
        '''
Exercise: 4x4s (Boulder Edition)

Objective: Develop aerobic power through back-to-back high-intensity climbs.
Climbing Details:
- Duration: Depends on the boulder problems selected.
- Move Count: Varies. Use 4 different boulder problems.
- Intensity: High
- Mode: Bouldering. Climb 4 problems consecutively without rest.
- Falls: Get back on immediately.
Rest Details: Short rests between sets, typically 1-3 minutes.
Repetitions: 4 sets of the 4-problem sequence. Adjust based on desired volume.
        '''
    ],
    'Anaerobic Capacity': [
        '''
Exercise: Long Boulders

Objective: Develop anaerobic capacity through intense, longer-duration climbs.
Climbing Details:
- Duration: 30-50 seconds
- Move Count: 12-15 moves
- Intensity: Very high. Should feel like 9 out of 10.
- Mode: Bouldering problems or circuits that push your limits.
- Falls: If you fall, note where you fell, rest, and try again, aiming to progress further.
- Cruxes: Expect cruxes. They will challenge your capacity. If you repeatedly fail at the same crux, consider an alternative or technique adjustment.
Rest Details: Rest for 2-4 times the duration of your climb.
Repetitions: 8-10 (can be split into sets)
        ''',
        '''
Exercise: Power Intervals

Objective: Boost anaerobic capacity with flashable maximal effort climbs and short rest.
Climbing Details:
- Duration: 30-40 seconds
- Intensity: Maximal. Push yourself!
- Mode: Bouldering problems or sequences that are at or near your limit.
- Falls: Falling indicates you're pushing your limits. Rest briefly and try again, or adjust the problem's difficulty.
- Cruxes: This exercise is about pushing hard, so challenging moves are expected. Adjust technique or sequence as needed.
Rest Details: Rest for 1 minute between climbs.
Repetitions: 8-10
        ''',
        '''
Exercise: Climbing Bursts

Objective: Improve anaerobic capacity by executing short, intense bursts of climbing movements.
Climbing Details:
- Duration: 20 seconds per burst
- Move Count: 6-8 explosive moves
- Intensity: High; choose moves that require power and precision.
- Mode: Bouldering problems that emphasize dynamic and powerful movements.
Rest Details: Rest for 2-3 minutes between bursts.
Repetitions: 6-8 bursts
        '''
    ],
    'Anaerobic Power': [
        '''
Exercise: Maximal Intensity Climbs

Objective: Develop anaerobic power through short, maximal effort climbs.
Climbing Details:
- Duration: 10-15 seconds
- Move Count: 3-5 moves
- Intensity: Maximal. Push your limits!
- Mode: Short bouldering problems or sequences that are slightly above your limit.
- Falls: Falling is common as you're pushing your boundaries. Take note of where and try to improve on the next attempt.
- Cruxes: Cruxes are expected. Experiment with different techniques to overcome them.
Rest Details: Rest for 10 minutes between climbs, ensuring full recovery.
Repetitions: 5-8
        ''',
        '''
Exercise: Dynamic Movements

Objective: Focus on power development through dynamic, explosive movements.
Climbing Details:
- Duration: 5-10 seconds
- Intensity: Maximal. Emphasize explosive power.
- Mode: Bouldering problems or sequences emphasizing dynamic moves, jumps, or campusing.
- Falls: Falling is expected, especially when trying dynamic moves. Ensure safe landing zones.
- Cruxes: This is about power, so don't get bogged down on cruxes. If a move repeatedly stops you, adjust your approach or technique.
Rest Details: Rest for 2-3 minutes between climbs.
Repetitions: 6-8
        ''',
        '''
Exercise: Limit Bouldering

Objective: Push your boundaries by working on the hardest moves or sequences you can attempt.
Climbing Details:
- Duration: Varies, but focus on 1-3 very challenging moves.
- Intensity: Maximal. This is about pushing your absolute limits.
- Mode: Bouldering problems or sequences that you find extremely challenging, perhaps even currently impossible.
- Falls: Expected. The goal is to push boundaries and try moves that might feel out of reach.
- Cruxes: The entire sequence is essentially a crux.
Rest Details: Rest for 4-5 minutes between attempts to ensure full recovery.
Repetitions: 5-6 attempts
        '''
    ]
}


    while True:
        print(f"\nChoose an exercise for {component}:")
        for idx, exercise in enumerate(exercises[component], 1):
            print("{}.".format(idx), exercise.split('\n')[1])  # Display the exercise name using str.format()

        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(exercises[component]):
                return exercises[component][choice - 1]
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number!")

def strength_training():
    exercises = {
    'Max Hangs': '''
Exercise: Max Hangs

Objective: Develop maximum finger strength through hangs at or near your maximum capacity.
Details:
- Hang Duration: 10 seconds
- Rest Duration: 3 minutes
- Sets: 5-6
- Intensity: Near maximum. Choose a weight that allows you to complete the hang, but just barely.
- Setup: Use a fingerboard with an edge depth you're comfortable with. Increase difficulty by reducing edge depth or adding weight.
- Execution: Maintain strict form, ensuring shoulders are engaged and not slouched. Use an open grip and avoid full crimping.
        ''',
    'Repeaters': '''
Exercise: Repeaters

Objective: Improve both strength and endurance in the fingers.
Details:
- Hang Duration: 7 seconds
- Rest between Hangs: 3 seconds
- Sets: 6 (1 set = 6 hangs)
- Rest between Sets: 3 minutes
- Intensity: Challenging but sustainable. Adjust weight or edge depth to maintain the challenge throughout the workout.
- Setup: Use a fingerboard with an edge depth you're comfortable with.
- Execution: Maintain proper form throughout each hang and during transitions.
        ''',
    'Aerobic Repeaters': '''
Exercise: Aerobic Repeaters

Objective: Enhance finger endurance through longer hangs and shorter rests at a low intensity.
Details:
- Hang Duration: 30 seconds
- Rest between Hangs: 30 seconds
- Sets: 4-5
- Intensity: Low. Focus on maintaining a relaxed grip and steady breathing.
- Setup: Use a fingerboard with an edge depth you're comfortable with.
- Execution: Keep a controlled pace, emphasizing endurance over strength.
        ''',
    'Power Repeaters': '''
Exercise: Power Repeaters

Objective: Increase finger strength and power with short, intense hangs and brief rests.
Details:
- Hang Duration: 10 seconds
- Rest between Hangs: 5 seconds
- Sets: 6 (1 set = 5-6 hangs)
- Rest between Sets: 3 minutes
- Intensity: Moderate. Push your limits with each hang while maintaining proper form.
- Setup: Use a fingerboard with an edge depth you're comfortable with.
- Execution: Execute each hang with maximum effort and explosiveness.
        ''',
    'Capacity Max Hangs': '''
Exercise: Capacity Max Hangs

Objective: Build finger strength endurance with longer hangs and shorter rests at high intensity.
Details:
- Hang Duration: 20 seconds
- Rest Duration: 2 minutes
- Sets: 5-6
- Intensity: High. Challenge yourself with the hang duration and minimal rest.
- Setup: Use a fingerboard with an edge depth you're comfortable with.
- Execution: Maintain form while focusing on enduring the extended hang duration.
        ''',
    'Power Max Hangs': '''
Exercise: Power Max Hangs

Objective: Develop explosive finger strength with very short, maximal effort hangs.
Details:
- Hang Duration: 5 seconds
- Rest Duration: 3 minutes
- Sets: 5-6
- Intensity: Maximal. Strive for maximum effort and power during each hang.
- Setup: Use a fingerboard with an edge depth you're comfortable with.
- Execution: Execute each hang with all-out intensity and explosiveness.
        '''
}

    while True:
        print("\nChoose a fingerboard exercise:")
        for idx, exercise in enumerate(exercises.keys(), 1):
            print("{}.".format(idx), exercise)  # Display the exercise name using str.format()

        try:
            choice = int(input("Enter the number corresponding to your choice: "))
            if 1 <= choice <= len(exercises):
                print(exercises[list(exercises.keys())[choice - 1]])
                if choice == 1:
                    fingerboard_max_hangs()
                elif choice == 2:
                    fingerboard_repeaters()
                elif choice == 3:
                    fingerboard_aerobic_repeaters()
                elif choice == 4:
                    fingerboard_power_repeaters()
                elif choice == 5:
                    fingerboard_capacity_max_hangs()
                elif choice == 6:
                    fingerboard_power_max_hangs()
                break
            else:
                print("Invalid choice. Please select a valid number.")
        except ValueError:
            print("Please enter a valid number!")


def workout_timer_with_beep(component, exercise):
    input("\nPress Enter When Ready...")
    if "Up-Down Climbing" in exercise:
        duration = 15 * 60  # 15 minutes in seconds
        timer_with_beep(10, "Get Ready for Up-Down Climbing")
        timer_with_beep(duration, "Climb up and down without resting")

    elif "Climbing Bursts" in exercise:
        reps = 6
        climb_time = 20
        rest_time = 180
        timer_with_beep(10, "Get Ready for Climbing Bursts")
        for _ in range(reps):
            timer_with_beep(climb_time, "Perform explosive climbing moves")
            timer_with_beep(rest_time, "Rest for 3 minutes")

    elif "Limit Bouldering" in exercise:
        reps = 5
        climb_time = get_climb_duration()
        rest_time = 300  # 5 minutes in seconds
        timer_with_beep(10, "Get Ready for Limit Bouldering")
        for _ in range(reps):
            timer_with_beep(climb_time, "Attempt the hardest moves or sequences")
            timer_with_beep(rest_time, "Rest for 5 minutes")

    elif "Continuous Climbing (ARC Training)" in exercise:
        duration = int(input("How many minutes do you want to climb for (suggested: 20-40 mins)? ")) * 60
        # 10-second setup timer
        timer_with_beep(10, "Get Ready")
        timer_with_beep(duration, "Climb at a constant intensity")

    elif "Moderate Intensity Climbing" in exercise:
        duration = int(input("How many minutes do you want to climb for (suggested: 10 mins)? ")) * 60
        # 10-second setup timer
        timer_with_beep(10, "Get Ready")
        timer_with_beep(duration, "Climb at a moderate intensity")

    elif "Circuits" in exercise:
        reps = int(input("How many reps do you want to perform (suggested: 3-4)? "))
        climb_time = get_climb_duration()
        rest_time = climb_time * 2  # Rest for double climb duration
        
        for _ in range(reps):
            timer_with_beep(10, "Get Ready for Circuits")
            timer_with_beep(climb_time, "Climb the circuit")
            timer_with_beep(rest_time, "Rest for twice the climbing time")

    elif "On-the-Minute" in exercise:
        reps = int(input("How many reps do you want to perform (suggested: 10-12)? "))
        climb_time = get_climb_duration()
        rest_time = 60 - climb_time
        timer_with_beep(10, "Get Ready for On the minute climbs")
        for _ in range(reps):
            timer_with_beep(climb_time, "Climb the boulder problem")
            timer_with_beep(rest_time, "Rest")

    elif "4x4s" in exercise:
        rounds = 4  # Always 4 rounds for 4x4s
        reps = 4  # 4 boulder problems per round
        climb_time = get_climb_duration()  # Duration for each boulder problem
        rest_time_round = 240  # Rest between rounds
        timer_with_beep(10, "Get Ready for 4x4s")
        for _ in range(rounds):
            for _ in range(reps):
                timer_with_beep(climb_time, "Climb the boulder problem")
            timer_with_beep(rest_time_round, "Rest between rounds")

    elif "Long Boulders" in exercise:
        reps = int(input("How many reps do you want to perform (suggested: 8-10)? "))
        climb_time = get_climb_duration()
        rest_multiplier = int(input("Enter rest time multiplier (suggested: 2-4 times the climb time): "))
        rest_time = climb_time * rest_multiplier
        # 10-second setup timer
        timer_with_beep(10, "Get Ready")
        for _ in range(reps):
            timer_with_beep(climb_time, "Climb the boulder problem or circuit")
            timer_with_beep(rest_time, "Rest")

    elif "Power Intervals" in exercise:
        reps = int(input("How many reps do you want to perform (suggested: 8-10)? "))
        climb_time = 35  # Adjusted to 30 seconds
        rest_time = 60
        timer_with_beep(10, "Get Ready")
        for _ in range(reps):
            timer_with_beep(climb_time, "Climb the boulder problem")
            timer_with_beep(rest_time, "Rest for 1 minute")

    elif "Maximal Intensity Climbs" in exercise:
        sets = int(input("How many sets do you want to perform (suggested: 4 after short bouldering, more if standalone)? "))
        reps_per_set = 4
        climb_time = get_climb_duration()
        rest_between_reps = climb_time  # Rest time between reps is equal to climb time
        rest_between_sets = 600  # 10 minutes in seconds
        timer_with_beep(10, "Get Ready for Maximal Intensity Climbs")
        for _ in range(sets):
            for _ in range(reps_per_set):
                timer_with_beep(climb_time, "Climb the hard boulder moves")
                if _ < reps_per_set - 1:  # Don't rest after the last rep of the set
                    timer_with_beep(rest_between_reps, f"Rest for {rest_between_reps} seconds")
            timer_with_beep(rest_between_sets, "Rest for 10 minutes")

    elif "Dynamic Movements" in exercise:
        reps = int(input("How many reps do you want to perform (suggested: 6-8)? "))
        climb_time = get_climb_duration()
        rest_time = 180  # 3 minutes in seconds
        # 10-second setup timer
        timer_with_beep(10, "Get Ready")
        for _ in range(reps):
            timer_with_beep(climb_time, "Focus on dynamic, explosive movements")
            timer_with_beep(rest_time, "Rest for 3 minutes")
    print("Workout complete!")

def main():
    try:
        user_grade = int(input("Enter your comfortable bouldering grade (e.g., for V4 enter 4): "))
    except ValueError:
        print("Please enter a valid number!")
        return

    print("\nChoose your type of training:")
    training_types = ["On-the-wall training", "Fingerboard training"]
    for idx, training_type in enumerate(training_types, 1):
        print(f"{idx}. {training_type}")
    
    training_choice = int(input("Enter the number corresponding to your choice: "))

    if training_choice == 1:
        # On-the-wall training
        print("\nChoose an energy system to train:")
        systems = ["Aerobic Capacity", "Aerobic Power", "Anaerobic Capacity", "Anaerobic Power"]
        for idx, system in enumerate(systems, 1):
            print(f"{idx}. {system}")
        
        while True:
            try:
                choice = int(input("Enter the number corresponding to your choice: "))
                if 1 <= choice <= 4:
                    selected_exercise = choose_exercise(systems[choice - 1])
                    recommended_boulder_grade = recommended_grade(user_grade, selected_exercise.split('\n')[1].split(':')[1].strip())
                    print(selected_exercise)
                    print(f"\nSuggested Grade: V{recommended_boulder_grade}")
                    workout_timer_with_beep(systems[choice - 1], selected_exercise)
                    break
                else:
                    print("Invalid choice. Please select a number between 1 and 4.")
            except ValueError:
                print("Please enter a valid number!")

    elif training_choice == 2:
        # Fingerboard training
        strength_training()

    else:
        print("Invalid choice. Please select a valid number.")


if __name__ == "__main__":
    main()
    print("Thank you for using the climbing workout tool based on the Training for Sport Climbing Paper by Alex Barrows! This implementation was made by Ted Bergstrand. Rest up! It's the most overlooked part of training.")
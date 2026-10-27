from pathlib import Path

import logic_user_interaction
import logic_weighting
import logic_data_injection as lg
import logs

while True:
    print("")
    print("Commands: (q)uit, (l)oad")
    user_input = input()

    if user_input == "":
        print("Commands: (q)uit, (l)oad")

    if user_input.lower() == "q":
        print("Quitting...")
        break

    if user_input.lower() == "l":
        user_path = Path(input("Enter path <path/to/file/file_name.extension>: ").strip(chr(34)))
        user_name = ""
        if not user_path.exists():
            user_name = Path(input("Enter file name <file_name.txt>: "))

        try:
            file = logic_user_interaction.InputFile(user_path, user_name).get_lines()

        except PermissionError as e:
            print(f"Error {e}")
            continue

        except OSError as e:
            print(f"Error {e}")
            continue

        if len(file) == 0:
            continue

        privacy_sensitivity = logic_weighting.privacy_probability(file)

        line_num = 0
        for line in file:
            line_num += 1
            sensitivity = logic_weighting.level_score(line)
            if 0.5 < sensitivity < 1.0:
                print(f"Line {line_num} contains possible sensitive information: ({sensitivity})\n{line[:30]}...")

            if 0.0 < sensitivity < 0.5:
                print(f"Line {line_num} contains very sensitive information: ({sensitivity})\n{line[:30]}... ")


        should_continue = False

        user_input = input("\n Should obfuscate searches? Y/N ")
        if user_input.lower() == "y":
            should_continue = True
        print("")

        if should_continue == True:
            lg.inject_searches(file)

        if user_input.lower() == "n":
            print("...")

    logs.measure_ram(Path(__file__).resolve().parent.parent / "logs")
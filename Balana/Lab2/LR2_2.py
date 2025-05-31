# LR2_2.py
# Lab 2
# 5/31/25
# Created by Balana, Francis Dominic G.
# Co-created by Github Copilot
# CPE106L-4-E02-02

# Function that defines the input of the user*

print("Greetings, I am a program that allows you to edit\nwhatever you want in a text file.\n\nPlease have your information ready.")

filename_edit = input("\nDesignate the filename: ")

try:
    with open(filename_edit, 'r') as file:
        lines = file.readlines()

except FileNotFoundError: # Exception for nonexistent files

    exit()

current = 0

while True:

    print(f"\nLine {current + 1}: {lines[current].rstrip()}")
    print("Options: [N]ext, [P]revious, [G]o to line, [Q]uit")
    choice = input("Choose an option: ").strip().lower()

    if choice == 'n':
        if current < len(lines) - 1:
            current += 1
        else:
            print("Already at the last line.")
    elif choice == 'p':
        if current > 0:
            current -= 1
        else:
            print("Already at the first line.")
    elif choice == 'g':
        try:
            line_num = int(input("Enter line number: ")) - 1
            if 0 <= line_num < len(lines):
                current = line_num
                print(f"\nLine {current + 1}: {lines[current].rstrip()}")
                while True:
                    sub_choice = input("Options: [E]dit, [R]eturn.\nChoose an option: ").strip().lower()
                    if sub_choice == 'e':
                        new_content = input("Enter new content for this line: ")
                        lines[current] = new_content + '\n'
                        print("Line updated.")
                    elif sub_choice == 'r':
                        break
                    else:
                        print("Invalid option.")
            else:
                print("Invalid line number.")
        except ValueError:
            print("Please enter a valid number.")
    elif choice == 'q':
        break
    else:
        print("Invalid option.")

# End of Code



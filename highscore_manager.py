def initialize_high_score(filename='highscore.txt'):
    try:
        with open(filename, 'r') as file:
            return int(file.read().strip())
    except FileNotFoundError:
        with open(filename, 'w') as file:
            file.write('0')
        return 0

def read_high_score(filename='highscore.txt'):
    with open(filename, 'r') as file:
        return int(file.read().strip())

def write_high_score(new_score, filename='highscore.txt'):
    with open(filename, 'w') as file:
        file.write(str(new_score))

def check_and_update_score(current_score, filename='highscore.txt'):
    high_score = read_high_score(filename)
    if current_score > high_score:
        print(f"New High Score: {current_score}")
        write_high_score(current_score, filename)
    else:
        print(f"Current High Score: {high_score}")
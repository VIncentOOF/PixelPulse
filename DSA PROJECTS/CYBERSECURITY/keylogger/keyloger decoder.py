decode_file = 'we.txt'

def read_content(file):
    with open(file, 'r') as f:
        return f.read().splitlines()

def append_current_word(current_word, result):
    if current_word:
        result.append(''.join(current_word))
        current_word.clear()

def process_line(line):
    return line.split(' - ')

def is_special_key(key):
    return key.lower() in {"space", "enter", "backspace", "shift", "ctrl", "alt", "tab"}

def handle_special_key(key, result, current_word):
    if key.lower() == "space":
        append_current_word(current_word, result)
        result.append(' ')
    elif key.lower() == "enter":
        append_current_word(current_word, result)
        result.append('\n')
    elif key.lower() == "backspace":
        if current_word:
            current_word.pop()
        elif result:
            if result[-1] in {' ', '\n'}:
                result.pop()
            else:
                result[-1] = result[-1][:-1]

def main(decode_file):
    content = read_content(decode_file)
    result = []
    current_word = []
    timestamps = []
    shift_active = False

    for line in content:
        timestamp, key = process_line(line)
        if not any(c.isalnum() for c in key):
            continue

        timestamps.append(timestamp)

        if is_special_key(key):
            if key.lower() == "shift":
                shift_active = True
            else:
                handle_special_key(key, result, current_word)
        else:
            if shift_active and len(key) == 1:
                key = key.upper()
                shift_active = False

            key_parts = key.split('-')
            if key_parts[0].lower() not in {"alt", "ctrl", "tab"}:
                current_word.append(key)

    append_current_word(current_word, result)

    final_result = ''.join(result)

    for i, (timestamp, key) in enumerate(zip(timestamps, result)):
        print(f"{timestamp}: {key}")

    print("\nFinal output:")
    print(final_result)

if __name__ == "__main__":
    main(decode_file)

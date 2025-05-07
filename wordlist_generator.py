import os
from itertools import product
from colorama import init, Fore, Style
from pyfiglet import Figlet
import shutil
import sys

# Initialize colorama for colored text in terminal
init(autoreset=True)

def print_banner():
    # Get terminal width
    terminal_width = shutil.get_terminal_size().columns

    # Use pyfiglet to render the project name "Banty" with block font
    figlet = Figlet(font='block')
    project_name = figlet.renderText('Banty').rstrip()  # Remove trailing whitespace
    
    # Center each line of the pyfiglet output
    project_lines = project_name.split('\n')
    centered_project = []
    for line in project_lines:
        padding = (terminal_width - len(line)) // 2
        centered_line = ' ' * max(0, padding) + line
        centered_project.append(centered_line)

    # Create and center the border
    border = '*' * (terminal_width // 2)
    centered_border = border.center(terminal_width)

    # Print the centered border, project name, and border again
    print(Fore.CYAN + centered_border + Style.RESET_ALL)
    for line in centered_project:
        print(Fore.CYAN + line + Style.RESET_ALL)
    print(Fore.CYAN + centered_border + Style.RESET_ALL)

    # Center the "=== Wordlist Generator ===" title
    title = "=== Wordlist Generator ==="
    padding = (terminal_width - len(title)) // 2
    centered_title = ' ' * max(0, padding) + title
    print(Fore.GREEN + centered_title + Style.RESET_ALL)

    # Center the project info box
    box = """
    ╔════════════════════════════════════╗
    ║     Wordlist Generator v1.0        ║
    ║     Developer: M.H.P.Lakshan       ║
    ║     Modes:                         ║
    ║       1. Simple Combination        ║
    ║       2. Semi-Split                ║
    ║       3. Full Breakdown            ║
    ╚════════════════════════════════════╝
    """
    box_lines = box.split('\n')
    centered_box = []
    for line in box_lines:
        padding = (terminal_width - len(line.rstrip())) // 2
        centered_line = ' ' * max(0, padding) + line.rstrip()
        centered_box.append(centered_line)
    
    # Print the centered box
    for line in centered_box:
        print(Fore.YELLOW + line + Style.RESET_ALL)

def split_phone(phone):
    return [phone[i:i+2] for i in range(0, len(phone), 2)]

def split_text(text):
    return text.replace(",", " ").replace("-", " ").split()

def leetspeak_variants(word):
    """Generate all possible leetspeak variants for a word."""
    subs = {'a': ['a', '@', '4'], 'e': ['e', '3'], 'i': ['i', '1'], 'o': ['o', '0'], 's': ['s', '$', '5'], 't': ['t', '7']}
    
    def generate_variants(current, pos, base):
        if pos == len(base):
            yield current
            return
        char = base[pos].lower()
        options = subs.get(char, [char])
        for opt in options:
            new_char = opt if char in subs else (base[pos] if base[pos].isupper() else opt)
            yield from generate_variants(current + new_char, pos + 1, base)
    
    return set(''.join(variant) for variant in generate_variants('', 0, word))

def case_variants(word):
    """Generate lowercase and uppercase variants of a word."""
    return {word.lower(), word.upper()}

def collect_info(title=""):
    print(Fore.YELLOW + f"\n-- {title} Information --" + Style.RESET_ALL)
    info = {
        'first_name': input(Fore.GREEN + "First Name (or press Enter to skip): " + Style.RESET_ALL).strip() or "unknown",
        'last_name': input(Fore.GREEN + "Last Name (or press Enter to skip): " + Style.RESET_ALL).strip() or "unknown",
        'nickname': input(Fore.GREEN + "Nickname (or press Enter to skip): " + Style.RESET_ALL).strip() or "unknown",
        'year': input(Fore.GREEN + "Birth Year (YYYY, or press Enter to skip): " + Style.RESET_ALL).strip(),
        'month': input(Fore.GREEN + "Birth Month (MM, or press Enter to skip): " + Style.RESET_ALL).strip(),
        'day': input(Fore.GREEN + "Birth Day (DD, or press Enter to skip): " + Style.RESET_ALL).strip(),
        'address': input(Fore.GREEN + "Address (or press Enter to skip): " + Style.RESET_ALL).strip() or "unknown",
        'email': input(Fore.GREEN + "Email (or press Enter to skip): " + Style.RESET_ALL).strip() or "unknown",
        'phone': input(Fore.GREEN + "Phone Number (or press Enter to skip): " + Style.RESET_ALL).strip() or "0000000000"
    }
    if info['year'] and (not info['year'].isdigit() or len(info['year']) != 4):
        print(Fore.RED + "⚠ Invalid year format. Using default '2000'." + Style.RESET_ALL)
        info['year'] = "2000"
    if info['month'] and (not info['month'].isdigit() or len(info['month']) != 2 or int(info['month']) > 12):
        print(Fore.RED + "⚠ Invalid month format. Using default '01'." + Style.RESET_ALL)
        info['month'] = "01"
    if info['day'] and (not info['day'].isdigit() or len(info['day']) != 2 or int(info['day']) > 31):
        print(Fore.RED + "⚠ Invalid day format. Using default '01'." + Style.RESET_ALL)
        info['day'] = "01"
    return info

def get_other_keywords():
    keywords = input(Fore.GREEN + "\nEnter other custom keywords (comma-separated, or press Enter to skip): " + Style.RESET_ALL).strip()
    return [w.strip() for w in keywords.split(',') if w.strip()] or []

def get_special_chars():
    response = input(Fore.GREEN + "Use special characters like @, &? (yes/no): " + Style.RESET_ALL).lower()
    return ['@', '&'] if response.startswith("y") else []

def build_wordlist(personal, friend, others, special_chars, mode, max_length=16):
    wordlist = set()

    def process_words(words):
        final = set()
        for w in words:
            w = w.strip()
            if not w: continue
            for case_var in case_variants(w):
                if len(case_var) <= max_length:
                    final.add(case_var)
                    for leet_var in leetspeak_variants(case_var):
                        if len(leet_var) <= max_length:
                            final.add(leet_var)
        return final

    if mode == 1:
        base = [
            personal['first_name'], personal['last_name'], personal['nickname'], personal['email'], personal['address'],
            friend['first_name'], friend['last_name'], friend['nickname'], friend['email'], friend['address']
        ]
        extra = [
            personal['year'], personal['month'], personal['day'],
            friend['year'], friend['month'], friend['day'],
            *split_phone(personal['phone']), *split_phone(friend['phone']),
            *others, *special_chars
        ]
        base_words = base + extra

    elif mode == 2:
        base = [
            personal['first_name'], personal['last_name'], personal['nickname'], personal['email'], personal['address'],
            friend['email'], friend['address']
        ]
        extra = [
            friend['first_name'], friend['last_name'], friend['nickname'],
            personal['year'], personal['month'], personal['day'],
            friend['year'], friend['month'], friend['day'],
            *split_phone(personal['phone']), *split_phone(friend['phone']),
            *others, *special_chars
        ]
        base_words = base + extra

    else:  # mode 3
        base_words = split_text(' '.join([
            personal['first_name'], personal['last_name'], personal['nickname'], personal['email'], personal['address'],
            friend['first_name'], friend['last_name'], friend['nickname'], friend['email'], friend['address']
        ])) + [
            personal['year'], personal['month'], personal['day'],
            friend['year'], friend['month'], friend['day'],
            *split_phone(personal['phone']), *split_phone(friend['phone']),
            *others, *special_chars
        ]

    final_words = process_words(base_words)
    print(Fore.YELLOW + f"\n🔧 Base word count (after leetspeak and case variants, max length {max_length}): {len(final_words)}" + Style.RESET_ALL)

    for i, (a, b) in enumerate(product(final_words, repeat=2), start=1):
        for combined in [a + b, b + a]:
            if len(combined) <= max_length:
                wordlist.add(combined)
        if i % 1000 == 0:
            print(Fore.MAGENTA + f"🔁 Processing combo #{i}" + Style.RESET_ALL)

    wordlist.update(final_words)
    print(Fore.YELLOW + f"\n✅ Total words generated (max length {max_length}): {len(wordlist)}" + Style.RESET_ALL)
    return wordlist

def validate_save_path(save_path):
    """Validate and prepare the save path."""
    save_path = os.path.expanduser(save_path)
    save_path = os.path.normpath(save_path)
    directory = os.path.dirname(save_path)
    
    if not directory:
        save_path = os.path.join(os.getcwd(), save_path)
        directory = os.getcwd()
    
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
            print(Fore.YELLOW + f"📁 Created directory: {directory}" + Style.RESET_ALL)
    except (OSError, PermissionError) as e:
        raise ValueError(f"Cannot create directory '{directory}': {e}")

    if not os.access(directory, os.W_OK):
        raise ValueError(f"No write permission for directory: {directory}")

    return save_path

def main():
    while True:
        print_banner()
        print(Fore.CYAN + "=== Wordlist Generator: 3 Modes (Enhanced) ===" + Style.RESET_ALL)

        personal = collect_info("Your")
        friend = collect_info("Friend's")
        other_keywords = get_other_keywords()
        special_chars = get_special_chars()

        print(Fore.CYAN + "\nChoose Wordlist Mode:\n1. Simple Combination\n2. Semi-Split\n3. Full Breakdown" + Style.RESET_ALL)
        try:
            mode = int(input(Fore.GREEN + "Enter mode number (1/2/3): " + Style.RESET_ALL).strip())
            if mode not in [1, 2, 3]:
                raise ValueError("Mode must be 1, 2, or 3")
        except ValueError as e:
            print(Fore.RED + f"❌ Invalid mode: {e}. Defaulting to mode 1." + Style.RESET_ALL)
            mode = 1

        default_filename = "wordlist.txt"
        save_path = input(Fore.GREEN + f"\nEnter full path to save the wordlist file (e.g., C:\\Users\\you\\Desktop\\wordlist.txt) or press Enter for default ({default_filename}): " + Style.RESET_ALL).strip()
        if not save_path:
            save_path = os.path.join(os.getcwd(), default_filename)
            print(Fore.YELLOW + f"Using default path: {save_path}" + Style.RESET_ALL)

        try:
            save_path = validate_save_path(save_path)
        except ValueError as e:
            print(Fore.RED + f"❌ Error with save path: {e}" + Style.RESET_ALL)
            print(Fore.RED + "Please ensure the path is valid and you have write permissions." + Style.RESET_ALL)
            continue

        print(Fore.MAGENTA + "\n🚀 Generating wordlist..." + Style.RESET_ALL)

        words = build_wordlist(personal, friend, other_keywords, special_chars, mode)

        print(Fore.MAGENTA + f"\n💾 Saving wordlist to: {save_path} ..." + Style.RESET_ALL)
        try:
            with open(save_path, "w", encoding='utf-8') as f:
                for word in sorted(words):
                    f.write(word + "\n")
            print(Fore.GREEN + f"\n🎉 Done! Wordlist saved at: {save_path}" + Style.RESET_ALL)
            print(Fore.GREEN + f"📊 Total words written: {len(words)}" + Style.RESET_ALL)
        except PermissionError:
            print(Fore.RED + f"❌ Permission denied: Cannot write to {save_path}. Check your permissions." + Style.RESET_ALL)
        except OSError as e:
            print(Fore.RED + f"❌ Error saving file: {e}. Ensure the path is valid and disk is not full." + Style.RESET_ALL)
        except Exception as e:
            print(Fore.RED + f"❌ Unexpected error: {e}. Please try a different path." + Style.RESET_ALL)

        if input(Fore.GREEN + "\nGenerate another wordlist? (yes/no): " + Style.RESET_ALL).lower().startswith('n'):
            print(Fore.CYAN + "\nThank you for using Wordlist Generator! Goodbye!" + Style.RESET_ALL)
            break

if __name__ == "__main__":
    main()
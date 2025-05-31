#!/usr/bin/env python3
"""
Zero-Knowledge Proof Demonstration
---------------------------------
This program demonstrates Schnorr's identification protocol, a zero-knowledge proof
where Alice proves to Bob that she knows a secret number x without revealing it.

"""

import random
import os
import sys
import time
import math
import shutil

# Get terminal size
terminal_width, terminal_height = shutil.get_terminal_size()

# Message history to maintain scrolling view
message_history = []
# How many messages to show in the history view
history_display_limit = 10

# Clear screen function that works on Windows, Mac, and Linux
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Add message to history
def add_to_history(message, color=None, side="center"):
    message_history.append((message, color, side))

# Function to print text with a typing effect
def type_text(text, delay=0.02, side="center", add_history=True):
    padding = 0
    if side == "left":
        padding = 2
        max_width = terminal_width // 2 - 4
    elif side == "right":
        padding = terminal_width // 2 + 2
        max_width = terminal_width // 2 - 4
    else:  # center
        max_width = terminal_width - 4
        
    # Split text into words
    words = text.split()
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the max width
        if len(current_line) + len(word) + 1 > max_width:
            # Print the current line
            print(" " * padding, end="")
            for char in current_line:
                print(char, end="", flush=True)
                time.sleep(delay)
            print()
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    
    # Print the last line
    if current_line:
        print(" " * padding, end="")
        for char in current_line:
            print(char, end="", flush=True)
            time.sleep(delay)
        print()
    
    # Add to history
    if add_history:
        add_to_history(text, None, side)

# Function to print colored text (works in most terminals)
def print_colored(text, color, side="center", add_history=True):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    padding = 0
    if side == "left":
        padding = 2
    elif side == "right":
        padding = terminal_width // 2 + 2
        
    print(f"{' ' * padding}{colors.get(color, '')}{text}{colors['reset']}")
    
    # Add to history
    if add_history:
        add_to_history(text, color, side)

def type_colored(text, color, side="center", delay=0.02, add_history=True):
    colors = {
        'red': '\033[91m',
        'green': '\033[92m',
        'yellow': '\033[93m',
        'blue': '\033[94m',
        'magenta': '\033[95m',
        'cyan': '\033[96m',
        'white': '\033[97m',
        'reset': '\033[0m'
    }
    
    padding = 0
    if side == "left":
        padding = 2
        max_width = terminal_width // 2 - 4
    elif side == "right":
        padding = terminal_width // 2 + 2
        max_width = terminal_width // 2 - 4
    else:  # center
        max_width = terminal_width - 4
        
    # Split text into words
    words = text.split()
    current_line = ""
    
    for word in words:
        # Check if adding this word would exceed the max width
        if len(current_line) + len(word) + 1 > max_width:
            # Print the current line
            print(" " * padding, end="")
            for char in current_line:
                print(f"{colors.get(color, '')}{char}{colors['reset']}", end="", flush=True)
                time.sleep(delay)
            print()
            current_line = word
        else:
            if current_line:
                current_line += " " + word
            else:
                current_line = word
    
    # Print the last line
    if current_line:
        print(" " * padding, end="")
        for char in current_line:
            print(f"{colors.get(color, '')}{char}{colors['reset']}", end="", flush=True)
            time.sleep(delay)
        print()
    
    # Add to history
    if add_history:
        add_to_history(text, color, side)

# Function to get a valid integer input from the user
def get_int_input(prompt, min_val=None, max_val=None, side="center", var_name=""):
    padding = 0
    if side == "left":
        padding = 2
    elif side == "right":
        padding = terminal_width // 2 + 2
    
    add_to_history(prompt, None, side)
    
    while True:
        try:
            print(" " * padding, end="")
            value = input(prompt)
            
            # Add input to history
            add_to_history(f"User input: {value}", "yellow", side)
            
            if value.lower() == 'r' or value.lower() == 'random':
                if min_val is not None and max_val is not None:
                    random_value = random.randint(min_val, max_val)
                    # Provide feedback about the randomly generated value with variable name
                    var_prefix = f"{var_name}=" if var_name else ""
                    random_msg = f"Randomly generated value: {var_prefix}{random_value}"
                    print(" " * padding + random_msg)
                    add_to_history(random_msg, "green", side)
                    
                    # Confirmation message in green
                    confirmation = f"✓ Using {var_prefix}{random_value} for the calculation"
                    print(" " * padding + "\033[92m" + confirmation + "\033[0m")
                    add_to_history(confirmation, "green", side)
                    
                    # Wait for user to press Enter
                    print(" " * padding, end="")
                    input("Press Enter to continue...")
                    
                    return random_value
                else:
                    print(" " * padding + "Cannot generate random value without range")
                    add_to_history("Cannot generate random value without range", "red", side)
                    continue
            value = int(value)
            if min_val is not None and value < min_val:
                error_msg = f"Please enter a value greater than or equal to {min_val}"
                print(" " * padding + error_msg)
                add_to_history(error_msg, "red", side)
                continue
            if max_val is not None and value > max_val:
                error_msg = f"Please enter a value less than or equal to {max_val}"
                print(" " * padding + error_msg)
                add_to_history(error_msg, "red", side)
                continue
                
            # For user-entered values, show confirmation
            var_prefix = f"{var_name}=" if var_name else ""
            confirmation = f"✓ Using {var_prefix}{value} for the calculation"
            print(" " * padding + "\033[92m" + confirmation + "\033[0m")
            add_to_history(confirmation, "green", side)
            
            # Wait for user to press Enter
            print(" " * padding, end="")
            input("Press Enter to continue...")
            
            return value
        except ValueError:
            error_msg = "Please enter a valid integer or 'r' for random"
            print(" " * padding + error_msg)
            add_to_history(error_msg, "red", side)

# Function to calculate (base^exponent) % modulus efficiently
def mod_exp(base, exponent, modulus):
    result = 1
    base = base % modulus
    while exponent > 0:
        if exponent % 2 == 1:
            result = (result * base) % modulus
        exponent = exponent >> 1
        base = (base * base) % modulus
    return result

# Function to check if a number is probably prime
def is_probably_prime(n, k=5):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0:
        return False
    
    # Find r and d such that n-1 = 2^r * d, with d odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = mod_exp(a, d, n)
        if x == 1 or x == n - 1:
            continue
        for _ in range(r - 1):
            x = mod_exp(x, 2, n)
            if x == n - 1:
                break
        else:
            return False
    return True

# Function to find a primitive root modulo p
def find_primitive_root(p):
    if p == 2:
        return 1
    
    # Find prime factors of p-1
    factors = set()
    phi = p - 1
    
    # Find prime factors of phi
    for i in range(2, int(math.sqrt(phi)) + 1):
        while phi % i == 0:
            factors.add(i)
            phi //= i
    if phi > 1:
        factors.add(phi)
    
    # Test random numbers until we find a primitive root
    for g in range(2, p):
        is_primitive = True
        for factor in factors:
            if mod_exp(g, (p - 1) // factor, p) == 1:
                is_primitive = False
                break
        if is_primitive:
            return g
    
    return None  # Should not reach here for valid primes

def print_header():
    clear_screen()
    print_colored("=" * terminal_width, 'cyan', add_history=False)
    print_colored("ZERO-KNOWLEDGE PROOF DEMONSTRATION".center(terminal_width), 'cyan', add_history=False)
    print_colored("=" * terminal_width, 'cyan', add_history=False)

def print_split_header():
    print_colored("=" * terminal_width, 'cyan', add_history=False)
    alice_header = "ALICE (PROVER)".center(terminal_width // 2)
    bob_header = "BOB (VERIFIER)".center(terminal_width // 2)
    print(f"\033[95m{alice_header}\033[0m" + f"\033[94m{bob_header}\033[0m")
    print_colored("-" * terminal_width, 'cyan', add_history=False)

def print_values_box(values_dict, alice_knows, bob_knows):
    # Box characters
    h_line = "═"
    v_line = "║"
    tl_corner = "╔"
    tr_corner = "╗"
    bl_corner = "╚"
    br_corner = "╝"
    t_junction = "╦"
    b_junction = "╩"
    l_junction = "╠"
    r_junction = "╣"
    cross = "╬"
    
    # Color mapping for different types of values
    value_colors = {
        "p": "cyan",
        "g": "cyan",
        "x": "magenta",
        "Y": "green",
        "k": "magenta",
        "R": "green",
        "c": "blue",
        "s": "green",
    }
    
    # Print top border
    print(f"{tl_corner}{h_line * (terminal_width - 2)}{tr_corner}")
    
    # Print title
    title = " CURRENT VALUES "
    padding = (terminal_width - len(title) - 2) // 2
    print(f"{v_line}\033[1;33m{' ' * padding}{title}{' ' * (terminal_width - 2 - padding - len(title))}\033[0m{v_line}")
    
    # Print horizontal divider
    print(f"{l_junction}{h_line * (terminal_width - 2)}{r_junction}")
    
    # Group values by type
    protocol_values = {}
    computed_values = {}
    
    for key, val in values_dict.items():
        if any(key.startswith(prefix) for prefix in ["p ", "g ", "x ", "k ", "c "]):
            protocol_values[key] = val
        else:
            computed_values[key] = val
    
    # Print protocol values with appropriate colors
    if protocol_values:
        # Print section header
        section_title = " Protocol Values "
        padding = (terminal_width - len(section_title) - 2) // 2
        print(f"{v_line}\033[1;36m{' ' * padding}{section_title}{' ' * (terminal_width - 2 - padding - len(section_title))}\033[0m{v_line}")
        
        # Calculate column width
        num_cols = 3
        col_width = (terminal_width - 2 - (num_cols - 1) * 3) // num_cols
        
        # Print values in columns
        values_list = list(protocol_values.items())
        rows = (len(values_list) + num_cols - 1) // num_cols
        
        for row in range(rows):
            line = v_line
            for col in range(num_cols):
                idx = row + col * rows
                if idx < len(values_list):
                    key, val = values_list[idx]
                    # Determine color based on prefix
                    color_key = key.split()[0].lower() if " " in key else key.lower()
                    color = value_colors.get(color_key, "white")
                    colors = {
                        'red': '\033[91m',
                        'green': '\033[92m',
                        'yellow': '\033[93m',
                        'blue': '\033[94m',
                        'magenta': '\033[95m',
                        'cyan': '\033[96m',
                        'white': '\033[97m',
                        'reset': '\033[0m'
                    }
                    entry = f"{key}: {colors.get(color, '')}{val}{colors['reset']}"
                    line += f" {entry.ljust(col_width)} "
                else:
                    line += " " * (col_width + 2)
                if col < num_cols - 1:
                    line += " "
            line += v_line
            print(line)
    
    # Print computed values if any
    if computed_values:
        # Print section divider
        print(f"{l_junction}{h_line * (terminal_width - 2)}{r_junction}")
        
        # Print section header
        section_title = " Computed Values "
        padding = (terminal_width - len(section_title) - 2) // 2
        print(f"{v_line}\033[1;36m{' ' * padding}{section_title}{' ' * (terminal_width - 2 - padding - len(section_title))}\033[0m{v_line}")
        
        # Print values in columns
        values_list = list(computed_values.items())
        rows = (len(values_list) + num_cols - 1) // num_cols
        
        for row in range(rows):
            line = v_line
            for col in range(num_cols):
                idx = row + col * rows
                if idx < len(values_list):
                    key, val = values_list[idx]
                    # Determine color based on key
                    color_key = key.split()[0] if " " in key else key
                    color = value_colors.get(color_key, "green")
                    colors = {
                        'red': '\033[91m',
                        'green': '\033[92m',
                        'yellow': '\033[93m',
                        'blue': '\033[94m',
                        'magenta': '\033[95m',
                        'cyan': '\033[96m',
                        'white': '\033[97m',
                        'reset': '\033[0m'
                    }
                    entry = f"{key}: {colors.get(color, '')}{val}{colors['reset']}"
                    line += f" {entry.ljust(col_width)} "
                else:
                    line += " " * (col_width + 2)
                if col < num_cols - 1:
                    line += " "
            line += v_line
            print(line)
    
    # Print knowledge section divider
    print(f"{l_junction}{h_line * (terminal_width - 2)}{r_junction}")
    
    # Print what Alice and Bob know
    knowledge_title = " Knowledge Overview "
    padding = (terminal_width - len(knowledge_title) - 2) // 2
    print(f"{v_line}\033[1;36m{' ' * padding}{knowledge_title}{' ' * (terminal_width - 2 - padding - len(knowledge_title))}\033[0m{v_line}")
    
    # Calculate half width for Alice and Bob columns
    half_width = (terminal_width - 3) // 2
    
    # Print what Alice knows
    alice_knows_str = "ALICE KNOWS: " + ", ".join(alice_knows)
    bob_knows_str = "BOB KNOWS: " + ", ".join(bob_knows)
    
    print(f"{v_line} \033[95m{alice_knows_str.ljust(half_width)}\033[0m {v_line} \033[94m{bob_knows_str.ljust(half_width)}\033[0m {v_line}")
    
    # Print bottom border
    print(f"{bl_corner}{h_line * (terminal_width - 2)}{br_corner}")
    print()

def print_step_header(step_num, title):
    print()
    header_text = f"STEP {step_num}: {title}"
    print_colored(header_text.center(terminal_width), 'green')
    print_colored("-" * terminal_width, 'green')
    print()

def print_divider():
    divider = "│"
    print(divider.center(terminal_width))

def print_split_screen():
    for _ in range(terminal_height - 10):  # Leave space for header and footer
        left_side = "│".rjust(terminal_width // 2)
        right_side = "│".ljust(terminal_width // 2)
        print(left_side + right_side)

# Redraw the screen with fixed elements and scrolling messages
def redraw_screen(values, alice_knows, bob_knows, current_step=None, active_side=None):
    clear_screen()
    
    # Draw fixed elements (values box and split header)
    print_values_box(values, alice_knows, bob_knows)
    print_split_header()
    
    # Print current step if provided
    if current_step:
        step_num, title = current_step
        print_step_header(step_num, title)
        print()
    
    # Print active side indicator if provided
    if active_side:
        if active_side.lower() == "alice":
            print_colored(">> YOU ARE NOW PLAYING AS ALICE <<", 'magenta', "left", add_history=False)
        else:
            print_colored(">> YOU ARE NOW PLAYING AS BOB <<", 'blue', "right", add_history=False)
        print()
    
    # Print scrolling message history (limited to last N messages)
    if message_history:
        print_colored("--- MESSAGE HISTORY ---".center(terminal_width), 'yellow', add_history=False)
        print()
        
        # Calculate how many messages to display
        start_idx = max(0, len(message_history) - history_display_limit)
        
        # Print the messages
        for msg, color, side in message_history[start_idx:]:
            if color:
                print_colored(msg, color, side, add_history=False)
            else:
                # For non-colored messages, just print with appropriate padding
                padding = 0
                if side == "left":
                    padding = 2
                elif side == "right":
                    padding = terminal_width // 2 + 2
                    
                print(" " * padding + msg)
        
        print()

def wait_for_user_continue():
    input_text = "Press Enter to continue..."
    add_to_history(input_text)
    input(input_text)

def main():
    # Dictionary to store all values
    values = {}
    # Lists to track what Alice and Bob know
    alice_knows = []
    bob_knows = []
    
    print_header()
    
    # Introduction
    type_colored("Welcome to the Zero-Knowledge Proof Demonstration!", 'green')
    type_text("In this program, you will play both roles: Alice and Bob.")
    type_text("Alice wants to prove to Bob that she knows a secret number x without revealing it.")
    type_text("This demonstration uses Schnorr's identification protocol, a classic ZKP.")
    print()
    type_text("The UI is split into two sides: Alice (left) and Bob (right).")
    type_text("You'll switch between these roles during the demonstration.")
    type_text("At each step, you can enter 'r' or 'random' to let the program choose a random value.")
    print()
    wait_for_user_continue()
    
    # Clear the initial introduction from history for a clean start
    global message_history
    message_history = []
    
    # Setup parameters
    redraw_screen(values, alice_knows, bob_knows)
    
    type_colored("SETTING UP PARAMETERS", 'yellow')
    print()
    
    # Let the user choose the prime number p
    print_colored("First, we need a prime number p for our modular arithmetic.", 'white')
    print("You can choose a prime number or let the program select one for you.")
    print("For demonstration purposes, using a small prime (e.g., between 11 and 101) is recommended.")
    
    while True:
        redraw_screen(values, alice_knows, bob_knows)
        print_colored("SETTING UP PARAMETERS", 'yellow')
        print()
        print_colored("Choose a prime number p or enter 'r' for random:", 'white')
        
        p_input = input("\nEnter a prime number p (or 'r' for random): ")
        add_to_history(f"User input: {p_input}", "yellow")
        
        if p_input.lower() == 'r' or p_input.lower() == 'random':
            # Choose a random prime from a list of small primes
            small_primes = [11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101]
            p = random.choice(small_primes)
            random_msg = f"Randomly generated value: p={p}"
            print(random_msg)
            add_to_history(random_msg, "green")
            
            # Confirmation message in green
            confirmation = f"✓ Using p={p} for the calculation"
            print("\033[92m" + confirmation + "\033[0m")
            add_to_history(confirmation, "green")
            
            # Wait for user to press Enter
            input("Press Enter to continue...")
            
            break
        else:
            try:
                p = int(p_input)
                if is_probably_prime(p):
                    add_to_history(f"Confirmed that {p} is prime.", "green")
                    
                    # Confirmation message in green
                    confirmation = f"✓ Using p={p} for the calculation"
                    print("\033[92m" + confirmation + "\033[0m")
                    add_to_history(confirmation, "green")
                    
                    # Wait for user to press Enter
                    input("Press Enter to continue...")
                    
                    break
                else:
                    add_to_history(f"{p} is not a prime number. Please try again.", "red")
            except ValueError:
                add_to_history("Please enter a valid integer or 'r' for random.", "red")
    
    values["p (prime)"] = p
    alice_knows.append("p")
    bob_knows.append("p")
    
    # Find a generator g for the multiplicative group mod p
    add_to_history("\nFinding a generator g for the multiplicative group mod p...")
    #g = find_primitive_root(p)
    g = 2 #for testing purposes
    add_to_history(f"Found generator g = {g}", "green")
    
    values["g (generator)"] = g
    alice_knows.append("g")
    bob_knows.append("g")
    
    add_to_history(f"\nPublic parameters:", "green")
    add_to_history(f"p (prime number): {p}", "green")
    add_to_history(f"g (generator): {g}", "green")
    
    add_to_history("\nIn this protocol:", "white")
    add_to_history("- Alice knows a secret number x (the witness)")
    add_to_history("- Alice wants to prove to Bob that she knows x without revealing it")
    add_to_history("- Both Alice and Bob agree on public parameters p and g")
    
    wait_for_user_continue()
    
    # Step 1: Alice chooses a secret witness x
    current_step = (1, "Alice chooses a secret witness x")
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored("As Alice, you need to choose a secret number x (the witness).", 'magenta', "left")
    type_text("This is the secret value you want to prove you know without revealing it.", side="left")
    x = get_int_input("\nChoose your secret witness x (an integer between 1 and p-2) or 'r' for random: ", 1, p-2, "left", "x")
    
    values["x (Alice's secret)"] = x
    alice_knows.append("x")
    
    # Calculate Y
    Y = mod_exp(g, x, p) # Y= g^x mod p, using the mod_exp function
    values["Y (g^x mod p)"] = Y
    alice_knows.append("Y")
    bob_knows.append("Y")
    
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored(f"Alice calculates Y = {Y}", 'magenta', "left")
    type_colored("Alice publishes Y (but keeps x secret)", 'magenta', "left")
    type_text("In a real-world scenario, Y would be Alice's public key, and x would be her private key.", side="left")
    
    wait_for_user_continue()
    
    # Step 2: Alice chooses a random k and calculates R
    current_step = (2, "Alice generates a commitment")
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored("As Alice, you need to choose a random number k.", 'magenta', "left")
    type_text("This is a one-time random value used to create a commitment.", side="left")
    k = get_int_input("\nChoose a random number k (an integer between 1 and p-2) or 'r' for random: ", 1, p-2, "left", "k")
    
    values["k (Alice's random)"] = k
    alice_knows.append("k")
    
    # Calculate R
    R = mod_exp(g, k, p) # R = g^k mod p
    values["R (g^k mod p)"] = R
    # TODO: Update Alice's and Bob's knowledge
    alice_knows.append("R")
    bob_knows.append("R")

    
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored(f"Alice calculates R = {R}", 'magenta', "left")
    type_colored("Alice sends R to Bob as a commitment", 'magenta', "left")
    type_text("The commitment R hides information about k but commits Alice to this value.", side="left")
    type_text("This is similar to sealing a secret in an envelope without revealing it yet.", side="left")
    
    wait_for_user_continue()
    
    # Step 3: Bob sends a challenge c to Alice
    current_step = (3, "Bob sends a challenge")
    redraw_screen(values, alice_knows, bob_knows, current_step, "Bob")
    
    type_colored("As Bob, you need to choose a random challenge c.", 'blue', "right")
    type_colored(f"Bob knows the public values:", 'blue', "right")
    type_colored(f"- p = {p} (prime number)", 'blue', "right")
    type_colored(f"- g = {g} (generator)", 'blue', "right")
    type_colored(f"- Y = {Y} (Alice's public key)", 'blue', "right")
    type_colored(f"- R = {R} (Alice's commitment)", 'blue', "right")
    
    c = get_int_input("\nChoose a random challenge c (an integer between 1 and p-2) or 'r' for random: ", 1, p-2, "right", "c")
    
    values["c (Bob's challenge)"] = c
    # TODO: Update Alice's and Bob's knowledge
    alice_knows.append("c")
    bob_knows.append("c")
    
    redraw_screen(values, alice_knows, bob_knows, current_step, "Bob")
    
    type_colored(f"Bob sends challenge c = {c} to Alice", 'blue', "right")
    type_text("The challenge c is Bob's way of ensuring Alice isn't cheating.", side="right")
    type_text("It's like asking Alice to solve a puzzle that depends on her secret.", side="right")
    
    wait_for_user_continue()
    
    # Step 4: Alice calculates s according to the protocol
    current_step = (4, "Alice responds to the challenge")
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored("As Alice, you need to calculate a response to Bob's challenge.", 'magenta', "left")
    type_colored(f"Alice has received challenge c = {c} from Bob", 'magenta', "left")
    
    # Calculate s according to the protocol
    s = k + (c*x) % (p-1)   # s = k + c*x mod (p-1)
    values["s (Alice's response)"] = s
    alice_knows.append("s")
    bob_knows.append("s")

    
    redraw_screen(values, alice_knows, bob_knows, current_step, "Alice")
    
    type_colored(f"Alice calculates s", 'magenta', "left")
    type_colored(f"s = {s}", 'magenta', "left")
    type_colored("Alice sends s to Bob", 'magenta', "left")
    type_text("The response s combines Alice's secret x with the random k and challenge c.", side="left")
    type_text("It reveals nothing about x by itself, but allows Bob to verify Alice knows x.", side="left")
    
    wait_for_user_continue()
    
    # Step 5: Bob verifies the proof
    current_step = (5, "Bob verifies the proof")
    redraw_screen(values, alice_knows, bob_knows, current_step, "Bob")
    
    type_colored("As Bob, you will now verify Alice's proof.", 'blue', "right")
    type_colored(f"Bob has received s = {s} from Alice", 'blue', "right")
    
    # Bob verifies the proof provided by Alice
    left_side = mod_exp(g, s, p) #Left side = g^s mod p
    right_side = ((Y**c) * R) % p #Right side (Y^c * R) mod p
    
    values["g^s mod p"] = left_side
    values["Y^c * R mod p"] = right_side
    bob_knows.append("verification")
    
    redraw_screen(values, alice_knows, bob_knows, current_step, "Bob")
    
    type_colored("Bob checks if the equation holds:", 'blue', "right")
    type_colored(f"Left side  = {left_side}", 'blue', "right")
    type_colored(f"Right side = {right_side}", 'blue', "right")
    
    if left_side == right_side:
        type_colored("Verification SUCCESSFUL! ✓", 'green', "right")
        type_text("Bob is convinced that Alice knows x without learning its value.", side="right")
    else:
        type_colored("Verification FAILED! ✗", 'red', "right")
        type_text("There was an error in the protocol or calculations.", side="right")
    
    wait_for_user_continue()
    
    # Final explanation
    redraw_screen(values, alice_knows, bob_knows)
    
    # Mathematical explanation
    print_colored("Mathematical verification:", 'yellow')
    type_text("If Alice knows x and follows the protocol, the verification will always succeed because:")
    type_text("TODO: fill in the explanation")
    
    # Explanation of why this is zero-knowledge
    print()
    print_colored("Why is this a zero-knowledge proof?", 'yellow')
    type_text("1. Completeness: If Alice knows the secret she can always convince Bob")
    type_text("2. Soundness: If Alice doesn't know the secret, she cannot convince Bob (except with negligible probability)")
    type_text("3. Zero-knowledge: Bob learns no additional knowledge about Alice's secret from the interaction")
    
    print()
    type_text("The protocol is zero-knowledge because the transcript (R, c, s) could be simulated")
    type_text("by anyone without knowing x, so it reveals no information about x.")
    
    print()
    print_colored("=" * terminal_width, 'cyan')
    print_colored("ZKP DEMONSTRATION COMPLETE".center(terminal_width), 'cyan')
    print_colored("=" * terminal_width, 'cyan')


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram terminated by user.")
        sys.exit(0)

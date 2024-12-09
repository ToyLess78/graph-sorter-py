import os
from collections import defaultdict, deque


# Validate the input file
def validate_file(file_path):
    # Check if the file has .txt extension
    if not file_path.endswith('.txt'):
        raise ValueError("Invalid file format. The file must be a .txt file.")

    # Check if the file exists
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"The file '{file_path}' does not exist.")

    # Read and validate each line in the file
    with open(file_path, 'r') as file:
        lines = file.read().splitlines()

    # Ensure all lines contain 6-digit numbers
    for line in lines:
        if not line.isdigit() or len(line) != 6:
            raise ValueError(f"Invalid line in file: '{line}'. Each line must be a 6-digit number.")

    print("File validation successful.")
    return lines


# Build a graph where each piece connects to others
def build_graph(pieces):
    graph = defaultdict(list)
    for i, piece1 in enumerate(pieces):
        for j, piece2 in enumerate(pieces):
            if i != j:  # Avoid self-loops
                if piece1[-2:] == piece2[:2]:  # Match condition: last 2 of piece1 = first 2 of piece2
                    graph[piece1].append(piece2)
    return graph


# Find the longest path in the graph using BFS
def find_longest_path(graph, start_piece):
    queue = deque([(start_piece, [start_piece])])  # Queue stores (current_node, current_path)
    longest_path = []

    while queue:
        current, path = queue.popleft()

        # Update the longest path if the current path is longer
        if len(path) > len(longest_path):
            longest_path = path

        # Sort neighbors by the number of connections (stable sorting)
        for neighbor in sorted(graph[current], key=lambda x: (len(graph[x]), x), reverse=True):
            if neighbor not in path and current[-2:] == neighbor[:2]:  # Ensure sequence matches
                queue.append((neighbor, path + [neighbor]))

    return longest_path


# Improve the sequence by including remaining elements with strict validation
def improve_with_remaining(pieces, main_sequence):
    # Find remaining pieces
    used = set(main_sequence)
    remaining = sorted(set(pieces) - used)  # Sort remaining pieces for consistency

    # Integrate remaining pieces into the sequence
    for piece in list(remaining):
        # Add to the end if it matches
        if main_sequence[-1][-2:] == piece[:2]:  # Match at the end
            main_sequence.append(piece)
            remaining.remove(piece)
        # Add to the start if it matches
        elif main_sequence[0][:2] == piece[-2:]:  # Match at the start
            main_sequence.insert(0, piece)
            remaining.remove(piece)

    return main_sequence


# Validate the final sequence
def validate_sequence(sequence):
    for i in range(len(sequence) - 1):
        if sequence[i][-2:] != sequence[i + 1][:2]:
            return False, i  # Return False and the index where the error occurs
    return True, -1  # If valid, return True


# Merge the sequence into a single number string
def merge_sequence(sequence):
    if not sequence:
        return ""
    merged = sequence[0]  # Start with the first number
    for i in range(1, len(sequence)):
        merged += sequence[i][2:]  # Append the remaining digits after the first two
    return merged


# Save the sorted sequence to a file
def save_sequence_to_file(sequence, output_file_path):
    with open(output_file_path, 'w') as file:
        for item in sequence:
            file.write(f"{item}\n")
    print(f"Sorted sequence saved to {output_file_path}")


# File paths
file_path = './source.txt'  # Update with your file path
output_file_path = './sortedlist.txt'

# Validate the file and load the data
try:
    numbers = validate_file(file_path)
except (ValueError, FileNotFoundError) as e:
    print(e)
    exit(1)

# Build the graph
graph = build_graph(numbers)

# Determine a valid starting piece
start_piece = min((piece for piece, connections in graph.items() if len(connections) == 1), default=numbers[0])

# Find the longest path
longest_path = find_longest_path(graph, start_piece)

# Improve the sequence by including remaining elements
final_sequence = improve_with_remaining(numbers, longest_path)

# Validate the final sequence
is_valid, error_index = validate_sequence(final_sequence)

# Print the results
print(f"Total pieces: {len(final_sequence)}")
print(f"Sequence is valid: {is_valid}")
if not is_valid:
    print(f"Error at index {error_index}: {final_sequence[error_index]} -> {final_sequence[error_index + 1]}")
else:
    print("The sequence is fully valid.")

# Merge the final sequence into a single string
merged_sequence = merge_sequence(final_sequence)
print(f"Final sequence: {merged_sequence}")

# Save the final sequence to a file
if is_valid:
    save_sequence_to_file(final_sequence, output_file_path)
else:
    print("The sequence is invalid. Not saving to file.")

import json

# Path to your input and output files
input_file = '/home/qasim/JFreaks/Scripts/codeFormatterJSON/input.json'
output_file = '/home/qasim/JFreaks/Scripts/codeFormatterJSON/output_formatted.txt'  # Use .txt extension for text formatting

# Read data from input file
with open(input_file, 'r') as f:
    data = json.load(f)

# Format the data as a JSON string
formatted_json = json.dumps(data, indent=4)

# Convert to the desired format with backticks and commas
formatted_lines = []
for line in formatted_json.splitlines():
    # Preserve leading spaces and add backticks, then add comma outside
    formatted_lines.append(f"`{line.rstrip()}`,")

# Join the lines with newline characters
formatted_output = "\n".join(formatted_lines)

# Write formatted output to text file
with open(output_file, 'w') as f:
    f.write(formatted_output)

print(f'Formatted data has been written to {output_file}')

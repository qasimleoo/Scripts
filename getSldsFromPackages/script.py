import re

# Function to extract keys associated with "DnsParser" from the input file
def extract_slds_with_dnsparser(input_file, output_file):
    with open(input_file, 'r') as infile:
        lines = infile.readlines()
        
        # Open the output file
        with open(output_file, 'w') as outfile:
            for line in lines:
                if "DnsParser" in line:
                    # Regex to extract the key (SLD), allowing for multiple dots
                    match = re.search(r'classesPackage\.put\("([\w-]+\.[\w.-]+)"', line)
                    if match:
                        sld = match.group(1)
                        outfile.write(sld + '\n')

# Input and output file paths
input_file = 'input.txt'   # Replace with your input file path
output_file = 'output.txt' # Replace with your desired output file path

# Call the function
extract_slds_with_dnsparser(input_file, output_file)

# Read the domains from the file
with open('/home/qasim/JFreaks/Scripts/domainsFormatBulk/domains.txt', 'r') as file:
    domains = file.read().splitlines()

# Format the domains as a list of quoted strings
formatted_domains = [f'"{domain}"' for domain in domains if domain != '']

# Join the formatted domains into a single string with commas
output = ",\n".join(formatted_domains)

# Write the formatted output to a new file
with open('/home/qasim/JFreaks/Scripts/domainsFormatBulk/domains.txt', 'w') as output_file:
    output_file.write(output)

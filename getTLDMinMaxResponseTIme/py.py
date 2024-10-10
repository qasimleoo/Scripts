import re

file_path = "/home/qasim/JFreaks/Scripts/getTLDMinMaxResponseTIme/file"
output_file_path = "/home/qasim/JFreaks/Scripts/getTLDMinMaxResponseTIme/output.txt"

with open(file_path, 'r') as file:
    log_data = file.read()

pattern = r'(?:whois=live).*?domainName=([^&\s]+).*?HTTP/1\.1" 200 .*?(\d+\.\d+)$|(?:domainName=([^&\s]+).*?whois=live).*?HTTP/1\.1" 200 .*?(\d+\.\d+)$'

matches = re.findall(pattern, log_data, re.MULTILINE)

response_times = {}
for match in matches:
    domain = match[0] or match[2]
    response_time = float(match[1] or match[3])
    tld = domain.split('.')[-1]

    if tld not in response_times:
        response_times[tld] = {
            'min_time': response_time,
            'min_domain': domain,
            'max_time': response_time,
            'max_domain': domain
        }
    else:
        if response_time < response_times[tld]['min_time']:
            response_times[tld]['min_time'] = response_time
            response_times[tld]['min_domain'] = domain
        if response_time > response_times[tld]['max_time']:
            response_times[tld]['max_time'] = response_time
            response_times[tld]['max_domain'] = domain

data = []
max_domain_length = 40

def trim_domain(domain, max_length):
    return domain if len(domain) <= max_length else '...' + domain[-(max_length - 3):]

for tld, times in response_times.items():
    min_domain = trim_domain(times['min_domain'], max_domain_length)
    max_domain = trim_domain(times['max_domain'], max_domain_length)

    if times['min_time'] == times['max_time']:
        data.append([tld, times['min_time'], min_domain, '-', '-'])
    else:
        data.append([tld, times['min_time'], min_domain, times['max_time'], max_domain])

# Prepare the table output
output_lines = []
header = f"| {'TLD':<10} | {'Min Response Time':<30} | {'Min Response Domain':<40} | {'Max Response Time':<30} | {'Max Response Domain':<40} |"
separator = '-' * len(header)

output_lines.append(separator)
output_lines.append(header)
output_lines.append(separator)

for row in data:
    output_lines.append(f"| {row[0]:<10} | {row[1]:<30} | {row[2]:<40} | {row[3]:<30} | {row[4]:<40} |")
output_lines.append(separator)

# Write to output file
with open(output_file_path, 'w') as output_file:
    output_file.write('\n'.join(output_lines))

print(f"Output written to {output_file_path}")

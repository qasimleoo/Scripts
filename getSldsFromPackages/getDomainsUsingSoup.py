from serpapi import GoogleSearch

# Function to search for SLDs and get the first three URLs
def google_search_slds(sld_list, serp_api_key):
    search_results = {}

    for sld in sld_list:
        query = f'site:*.{sld}'
        params = {
            "q": query,
            "num": 3,  # Number of results to return
            "api_key": serp_api_key
        }
        
        print(query)
        print(params)


        search = GoogleSearch(params)
        results = search.get_dict()
        print(results)
        search_results[sld] = [result['link'] for result in results['organic_results'][:3]]
    
    return search_results

# Input and output file paths
input_file = '/home/qasim/JFreaks/Scripts/getSldsFromPackages/output.txt'  # File containing the extracted SLDs
output_file = 'search_results.txt'  # File to save the search results
serp_api_key = 'AIzaSyBoPhw9H2daYI4Grw_ZclsSxljcj1f8tq8'  # Replace with your SerpAPI key

# Read the SLDs from the output file
with open(input_file, 'r') as infile:
    slds = [line.strip() for line in infile.readlines()]

# Perform Google search for each SLD and get the first three URLs
results = google_search_slds(slds, serp_api_key)

# Write the search results to the output file
with open(output_file, 'w') as outfile:
    for sld, urls in results.items():
        outfile.write(f'{sld}:\n')
        for url in urls:
            outfile.write(f'{url}\n')
        outfile.write('\n')

import requests
import json
import re

# Fetch the JSON data from the API
response = requests.get('https://tplayapi.code-crafters.app/321codecrafters/fetcher.json')
input_json = response.json()

# Function to perform replacements
def replace_urls(channel):
    if 'manifest_url' in channel:
        # Replace delta and bpweb with bpprodchannel['manifest_url'] = channel['manifest_url'].replace('delta', 'bpprod').replace('bpweb', 'bpprod').replace('tatasky.akamaized.net', 'catchup.akamaized.net')
    
        url = channel['manifest_url'].replace('delta', 'bpprod').replace('bpweb', 'bpprod').replace('tatasky.akamaized.net', 'catchup.akamaized.net')
        # Replace <number>.akamaized.net with catchup.akamaized.net preserving the number
        url = re.sub(r'(\d+)\.akamaized\.net', r'\1catchup.akamaized.net', url)
        channel['manifest_url'] = url
    return channel

# Replace URLs in all channels
channels = input_json['data']['channels']
customized_channels = [replace_urls(channel) for channel in channels]

# Prepare the final output format
output_json = {}
for i, channel in enumerate(customized_channels, 1):
    if 'clearkeys' in channel and channel['clearkeys']:
        clearkey = channel['clearkeys'][0]  # Use only the first clearkey
        key_info = {
            'clearkey': clearkey['hex'],
            'url': channel['manifest_url']
        }
        output_json[f'{channel["id"]}'] = key_info


# Save the output to a JSON file
with open('pta_nhi.json', 'w') as outfile:
    json.dump(output_json, outfile, indent=2)

# Print the result
print("File Saved Successfully")

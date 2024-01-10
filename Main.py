import requests
import yaml
import time

input_file = input("Enter the file name with absolute path: ")  # Get the absolute file path from the user
# input_file="fetch.yaml"
try: 
    with open(input_file, "r") as data:
        
        data = yaml.load(data, Loader=yaml.FullLoader)   # Load YAML data from the file
        
        counter_time = time.time()+15   # Set a 15-second timer for the health check cycle 
        # Set initial counters
        total_request_sent = 0
        up = 0
        down = 0
        domain_dict= {}   # Create Dictionary to store domain-specific metrics
        
        while time.time() < counter_time:   # Main loop: Run health checks every 15 seconds         
            for fetch in data:   # fetch configuration in the YAML file      
                if "url" not in fetch:   # Check if URL is present in the fetch data
                    print("URL not found " + str(fetch.get("name", "no-name")))
                    continue
                
                # Extract domain name from the URL
                url = fetch["url"]    
                domain = url.split('/')[2]

                # Send HTTP request to the endpoint
                response = requests.request(fetch.get("method", "GET"), url, data=fetch.get("body", None), headers=fetch.get("headers", None), timeout=15)
                latency = response.elapsed.total_seconds()*1000     # Calculate the latency of the response
                
                # Check the response and update metrics
                if response.status_code == 200 and latency < 500:
                    up += 1
                    if domain not in domain_dict:
                        domain_dict[domain]={}                    
                    domain_dict[domain]["up"]=up    # Assigning UP counter value to the dictionary
                elif response.status_code != 200 or latency > 500:
                    down += 1
                    if domain not in domain_dict:   # Checking for domian in the dictionary
                        domain_dict[domain]={}                    
                    domain_dict[domain]["down"]=down    # Assigning DOWN counter value to the dictionary               
                
                total_request_sent += 1
                domain_dict[domain]["total_request_sent"]=total_request_sent    # Assigning total request sent to the dictionary

            # Calculate the domain availability percentages after 15 seconds   
            if time.time() > counter_time:            
                for domain, metrics in domain_dict.items():                
                    print(domain+" has "+str(int((metrics.pop('up')/metrics.pop('total_request_sent'))*100))+"% availability")    
                counter_time = time.time()+15
                total_request_sent = 0
                up = 0
                down = 0
                domain_dict= {}

except KeyboardInterrupt:
    print("\nUser exited the program.")
except Exception as e:
    print(f"An error occurred: {str(e)}")

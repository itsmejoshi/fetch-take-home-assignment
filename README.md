## Overview
- This Python program is implemented to checks the health of a set of HTTP endpoints,calculates the availability percentage for each domain, and prints the metrics. The program reads an input YAML configuration file containing a list of HTTP endpoints.

## Requirements
- Python 3.x
- Requests & yaml library (`pip install requests yaml`)

## Parsing the program input
- A sample YAML file which contains a list of HTTP endpoints(name,url,method,headers,body)will be taken as a input and  loaded as a data

```
    input_file = input("Enter the file name with absolute path: ")

        with open(input_file, "r") as data:
            data = yaml.safe_load(data)

```
## Running the health checks
- Created a `counter_time` and added 15 seconds to the current time as we should send a HTTP request to the endpoints for every 15 seconds
- Initialise Up,Down,No of requests as zero ,they increment their count respectively if the conditions are true
- Created an empty dictionary to store the success,failed and total requests 
- Run the while loop with the condition current time should less than the counter time as it runs for every 15-seconds.
- Now for loop is used to get the url from the data which is YAML file and it checks for the Url,if url is not found it `continues` to get the next index from the loop,otherwise it stores the url.`split` method is used to separate domain name from the URL as we need to calculate the availability percentage of only domains.
- Now code sends an HTTP request to a specified URL using the `request` library and recieves the response of HTTP method, URL of the HTTP endpoint, Data, HTTP Headers from the configuration
- `timeout` is used, which specifies the maximum time (in seconds) the request is allowed to take. If the request exceeds this duration, a timeout exception will be raised.
- Calculate the `latency` from the response time and convert it into milliseconds.
- Now checks with the given conditions,If the status code is 200 (indicating a successful response) and the latency is less than 500 milliseconds, then ***updates UP counter*** which is considered as ***number of HTTP REQUESTS OF UP***.Now checks if that domain is available in domain_dict dictionary,if not then add the domain to the dictionary as a key, now add the information about the UP COUNT to the domain_dict dictionary under the key corresponding to the domain.Here _I used dictionary inside disctionary for storing the domain and its corresponding rquests as a key-value pair._

```
    if response.status_code == 200 and latency < 500:
        up += 1
        if domain not in domain_dict:
           domain_dict[domain]={}                    
        domain_dict[domain]["up"]=up
        elif response.status_code != 200 or latency > 500:
            down += 1
            if domain not in domain_dict:
                domain_dict[domain]={}                    
            domain_dict[domain]["down"]=down
        total_request_sent += 1
        domain_dict[domain]["total_request_sent"]=total_request_sent         
                
```
- If the status code is not 200 or the latency is greater than 500 milliseconds, it is considered a DOWN response. The down counter is incremented, and information about the DOWN count is stored in the domain_dict dictionary under the key corresponding to the domain.
- ***Incremented the total request sent counter*** to obtain ***total number of HTTP REQUESTS*** which includes UP and Down HTTP REQUESTS regardless of the conditon and stored its counter value in the domain_dict dictionary under the key corresponding to the domain.

## Printing the metrics
- If condition checks whether the current time has exceeded the counter_time.If true,it means that the specified time interval(15 seconds) has passed.
- Now run the **for loop** through each domain and its associated metrics in the `domain_dict`
- Calculate the ***Availability percentage** by using Number of requests of UP AND TOTAL NUMBER OF REQUESTS SENT.Here we used `pop()` method which is used in dictionary,it removes the total count of UP AND TOTAL REQUESTS from the domain_dict and calculate the availability percentage.Here we used int to make the float availability percentage to the nearest whole number.

```
    int((metrics.pop('up')/metrics.pop('total_request_sent'))*100)

```
- `counter_time = time.time() + 15` It resets the counter_time for the next interval,by adding 15 seconds to the current time.
- `total_request_sent = 0, up = 0, down = 0` These reset the counters for total requests, UP responses, and DOWN responses because to start fresh for the next time interval.`domain_dict = {}` clears the domain_dict, for resetting the storage for metrics related to each domain for the next interval.
-Implemented `KeyboardInterrupt` exception, if user exits the program manually by `CTRL+C`.
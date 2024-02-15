#Get important dependencies
#/usr/bin/python3
import sys
from collections import defaultdict

def read_access_log(file_name):
    user_agents = defaultdict(int)
    total_requests = 0

    try:
        with open(file_name, 'r') as file:
            for line in file:
                user_agent = line.strip().rsplit(' ', 1)[-1]
                user_agents[user_agent] += 1
                total_requests += 1
    except FileNotFoundError:
        print(f"File '{file_name}' not found.")
        sys.exit(1)

    return user_agents, total_requests

def main():
    if len(sys.argv) != 2:
        print("Please enter file name as described in the usage")
        print("Usage: python script_name.py <access_log_file>")
        sys.exit(1)

    file_name = sys.argv[1]
    user_agents, total_requests = read_access_log(file_name)

    print(f"Total number of different User Agents: {len(user_agents)}")
    print("Statistics:")
    for user_agent, requests in user_agents.items():
        print(f"{user_agent}: {requests} requests ({requests / total_requests:.2%} of total)")

if __name__ == "__main__":
    main()


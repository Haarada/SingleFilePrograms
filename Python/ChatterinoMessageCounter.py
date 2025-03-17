#!/usr/bin/env python3
import os
import argparse

# Scripts that counts messagess sent on Twitch chat, grouped by user.
# Based on Chatterino log files
# usage: count_messages.py [-h] [--users [USERS ...]] folder

# limits how many users are listed
max = 50

def count_messages(folder, specific_users=None):
    """
    Walks through all files in the given folder and counts messages.
    
    Parameters:
        folder (str): Path to the folder containing log files.
        specific_users (list or None): List of usernames to count. If None,
            counts for all users are returned.
    
    Returns:
        total_count (int): Total number of messages processed.
        user_counts (dict): Dictionary mapping usernames to their message count.
    """
    user_counts = {}
    total_count = 0

    # Loop over every file in the folder (non-recursive)
    for filename in os.listdir(folder):
        filepath = os.path.join(folder, filename)
        if not os.path.isfile(filepath):
            continue  # Skip subdirectories or non-files

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                for line in file:
                    line = line.strip()
                    if not line:
                        continue

                    # Skip header lines or comments that start with '#'
                    if line.startswith('#'):
                        continue

                    # Process only lines that start with '[' (indicating a log entry)
                    if not line.startswith('['):
                        continue

                    # Find the closing bracket for the timestamp.
                    closing_bracket = line.find(']')
                    if closing_bracket == -1:
                        continue  # Malformed line; skip it

                    # Get the rest of the line after the timestamp.
                    rest = line[closing_bracket+1:].strip()
                    if not rest:
                        continue

                    # Determine the username.
                    if ':' in rest:
                        username, _, _ = rest.partition(':')
                        username = username.strip()
                    else:
                        # When there’s no colon, assume the first word is the username.
                        username = rest.split()[0]

                    username = username.lower()
                    # Update the counts.
                    total_count += 1
                    user_counts[username] = user_counts.get(username, 0) + 1

        except Exception as err:
            print(f"Error reading {filepath}: {err}")

    # If specific users were provided, filter the results.
    if specific_users is not None:
        specific_counts = {user: user_counts.get(user, 0) for user in specific_users}
        return total_count, specific_counts

    return total_count, user_counts

def main():
    parser = argparse.ArgumentParser(
        description="Count total messages and messages from specific users in log files."
    )
    parser.add_argument(
        "folder",
        help="Path to the folder containing the log files."
    )
    parser.add_argument(
        "--users",
        nargs="*",
        help="List of specific usernames to count messages for. If not provided, all users are listed."
    )
    args = parser.parse_args()

    total, counts = count_messages(args.folder, specific_users=args.users)
    print(f"Total messages: {total}")
    
    # Sort the user counts by messages sent in descending order
    sorted_counts = sorted(counts.items(), key=lambda item: item[1], reverse=True)

    if args.users:
        print("Message counts for specified users (sorted by messages sent):")
    else:
        print("Message counts per user (sorted by messages sent):")
        
    cur = 1 
    for user, count in sorted_counts:
        print(f"  {user}: {count}")
        cur += 1
        if(cur >= max):
            break

if __name__ == "__main__":
    main()

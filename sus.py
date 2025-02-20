import os
import random
import subprocess
import datetime

def git_commit(message, commit_date):
    # Stage the changes
    subprocess.run(['git', 'add', 'deets.md'])

    # Create commit with specified date
    env = os.environ.copy()
    env['GIT_COMMITTER_DATE'] = commit_date.strftime('%Y-%m-%dT%H:%M:%S')
    subprocess.run(['git', 'commit', '-m', message, '--date', commit_date.strftime('%Y-%m-%dT%H:%M:%S')], env=env)

def git_push():
    # Push the changes to the remote repository
    subprocess.run(['git', 'push'])

# Main function to create files for a range of dates
def fake_commits(start_date, end_date, min_commits, max_commits, skipping=False, max_skip_days=1):
    file_path = "deets.md"  # Single file at the script's level

    current_date = start_date
    while current_date <= end_date:
        # skip days randomly, if skiping is enabled
        if skipping and random.choice([True, False]):
            skip_days = random.randint(0, max_skip_days)
            print(f"\n\nSkipping {skip_days} days from {current_date.strftime('%d-%b-%Y')}")
            current_date += datetime.timedelta(days=skip_days)
            continue

        # Random number of commits for the current date
        n_commits = random.randint(min_commits, max_commits)
        print(f"\n\n{n_commits} commits for date: {current_date.strftime('%d-%b-%Y')}")

        with open(file_path, "a") as file:  # Append mode
            for i in range(1, n_commits + 1):
                info = f"Date: {current_date.strftime('%d-%b-%Y')}, Commit #: {i}"
                with open(file_path, "w") as file:
                    file.write("")  # Clear the file
                    file.write(info)
                print(info)
                git_commit(info, current_date)

        # Move to the next day
        current_date += datetime.timedelta(days=1)

    # Push all the changes
    git_push()

def get_date_input(prompt):
    while True:
        date_str = input(prompt + " (YYYY-MM-DD): ")
        try:
            date = datetime.datetime.strptime(date_str, '%Y-%m-%d')
            return date
        except ValueError:
            print("Invalid date format. Please use YYYY-MM-DD.")

def get_int_input(prompt, min_val=None, max_val=None):
    while True:
        try:
            value = int(input(prompt + ": "))
            if min_val is not None and value < min_val:
                print(f"Value must be at least {min_val}.")
            elif max_val is not None and value > max_val:
                print(f"Value must be no more than {max_val}.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter an integer.")

def get_bool_input(prompt):
    while True:
        choice = input(prompt + " (y/n): ").lower()
        if choice in ['y', 'yes']:
            return True
        elif choice in ['n', 'no']:
            return False
        else:
            print("Invalid input. Please enter 'y' or 'n'.")

def main():
    print("Welcome to the Fake Commit Generator!")

    start_date = get_date_input("Enter the start date")
    end_date = get_date_input("Enter the end date")

    # Validate that end_date is not before start_date
    while end_date < start_date:
        print("End date cannot be before start date.  Please enter a valid end date.")
        end_date = get_date_input("Enter the end date")

    min_commits = get_int_input("Enter the minimum number of commits per day", min_val=1)
    max_commits = get_int_input("Enter the maximum number of commits per day", min_val=min_commits)  # Ensure max >= min
    skipping = get_bool_input("Enable skipping days?")
    max_skip_days = 0
    if skipping:
        max_skip_days = get_int_input("Enter the maximum number of days to skip", min_val=1)

    print("\nGenerating commits...\n")
    fake_commits(start_date, end_date, min_commits, max_commits, skipping, max_skip_days)
    print("\nCommits generated and pushed!")

if __name__ == "__main__":
    main()
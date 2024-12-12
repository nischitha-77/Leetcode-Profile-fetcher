# data.py

import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict

# LeetCode API URL and GraphQL Query
API_URL = "https://leetcode.com/graphql"
QUERY = """
query getUserProfile($username: String!) {
    matchedUser(username: $username) {
        username
        profile {
            ranking
        }
        submitStats {
            acSubmissionNum {
                difficulty
                count
            }
        }
        badges {
            displayName
        }
    }
}
"""

def fetch_user_profile(username: str) -> Dict:
    """Fetch details for a single LeetCode user."""
    try:
        response = requests.post(
            API_URL,
            json={"query": QUERY, "variables": {"username": username}},
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()  # Raise an error for HTTP response issues
        data = response.json()

        user = data["data"]["matchedUser"]
        if not user:
            return {
                "Username": username,
                "LeetCode Ranking": "N/A",
                "Easy": "N/A",
                "Medium": "N/A",
                "Hard": "N/A",
                "Total": "N/A",
                "Number of Badges": "0",
                "Badges": "None",
                "Profile URL": f"https://leetcode.com/{username}/"
            }

        ranking = user["profile"]["ranking"] or "N/A"
        submissions = user["submitStats"]["acSubmissionNum"]

        easy = medium = hard = 0
        for submission in submissions:
            if submission["difficulty"] == "Easy":
                easy = submission["count"]
            elif submission["difficulty"] == "Medium":
                medium = submission["count"]
            elif submission["difficulty"] == "Hard":
                hard = submission["count"]

        total = easy + medium + hard
        badges = [badge["displayName"] for badge in user["badges"]]
        number_of_badges = len(badges)
        badge_names = ", ".join(badges) if badges else "None"

        return {
            "Username": username,
            "LeetCode Ranking": ranking,
            "Easy": easy,
            "Medium": medium,
            "Hard": hard,
            "Total": total,
            "Number of Badges": number_of_badges,
            "Badges": badge_names,
            "Profile URL": f"https://leetcode.com/{username}/"
        }
    except Exception as e:
        return {
            "Username": username,
            "LeetCode Ranking": "Error",
            "Easy": "Error",
            "Medium": "Error",
            "Hard": "Error",
            "Total": "Error",
            "Number of Badges": "Error",
            "Badges": str(e),
            "Profile URL": f"https://leetcode.com/{username}/"
        }

# Fetch profiles concurrently for multiple users
def fetch_all_profiles(usernames: List[str]) -> List[Dict]:
    """Fetch profiles for multiple users concurrently."""
    profiles = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = {executor.submit(fetch_user_profile, username): username for username in usernames}
        for future in as_completed(futures):
            result = future.result()
            profiles.append(result)
    return profiles

# Sorting functions (unchanged)
def sort_by_ranking(data: List[Dict]) -> List[Dict]:
    """Sort the data by LeetCode ranking in increasing order."""
    for record in data:
        if record["LeetCode Ranking"] == "N/A" or record["LeetCode Ranking"] == "Error":
            record["LeetCode Ranking"] = float('inf')
        else:
            record["LeetCode Ranking"] = int(record["LeetCode Ranking"])

    sorted_data = sorted(data, key=lambda x: x["LeetCode Ranking"])

    for record in sorted_data:
        if record["LeetCode Ranking"] == float('inf'):
            record["LeetCode Ranking"] = "N/A"

    return sorted_data

def sort_by_problems_solved(data: List[Dict]) -> List[Dict]:
    """Sort the data by total problems solved in descending order."""
    for record in data:
        if record["Total"] == "N/A" or record["Total"] == "Error":
            record["Total"] = -1  # Set non-existent values to -1 for sorting
        else:
            record["Total"] = int(record["Total"])

    sorted_data = sorted(data, key=lambda x: x["Total"], reverse=True)

    for record in sorted_data:
        if record["Total"] == -1:
            record["Total"] = "N/A"

    return sorted_data

def sort_by_badges(data: List[Dict]) -> List[Dict]:
    """Sort the data by number of badges in descending order."""
    for record in data:
        if record["Number of Badges"] == "N/A" or record["Number of Badges"] == "Error":
            record["Number of Badges"] = -1
        else:
            record["Number of Badges"] = int(record["Number of Badges"])

    sorted_data = sorted(data, key=lambda x: x["Number of Badges"], reverse=True)

    for record in sorted_data:
        if record["Number of Badges"] == -1:
            record["Number of Badges"] = "N/A"

    return sorted_data

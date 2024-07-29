import requests
import os
import time
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
keywords_file = os.path.join(script_dir, 'keywords', 'keywords.py')

keywords = {}
with open(keywords_file, 'r') as file:
    exec(file.read(), keywords)

usernameKeywords = keywords['usernameKeywords']
descriptionKeywords = keywords['descriptionKeywords']
displayNameKeywords = keywords['displayNameKeywords']

def normalize_text(text):
    return text.lower().split()

def calculate_user_score(display_name, username, description):
    user_score = 0
    flag_reasons = []

    def check_keywords(text, keywords):
        nonlocal user_score, flag_reasons
        for keyword, info in keywords.items():
            if keyword.lower() in text:
                if isinstance(info, dict):
                    user_score += info["value"]
                    if "reason" in info:
                        flag_reasons.append(info["reason"])
                else:
                    user_score += info

    display_name_lower = display_name.lower()
    username_lower = username.lower()
    description_lower = description.lower()

    check_keywords(display_name_lower, displayNameKeywords)
    check_keywords(username_lower, usernameKeywords)
    check_keywords(description_lower, descriptionKeywords)

    return user_score, list(set(flag_reasons))  # Remove duplicate reasons

def fetch_roblox_profile(user_id):
    url = f"https://users.roblox.com/v1/users/{user_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

def fetch_group_members(group_id):
    members = []
    cursor = ""
    while True:
        url = f"https://groups.roblox.com/v1/groups/{group_id}/users?limit=100&sortOrder=Asc&cursor={cursor}"
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            members.extend(data["data"])
            cursor = data.get("nextPageCursor", "")
            if not cursor:
                break
        else:
            print(f"Error fetching group members: {response.status_code}")
            break
    return [member["user"]["userId"] for member in members]

# main
def analyze_profiles(user_ids):
    results = []
    total_users = len(user_ids)
    for count, user_id in enumerate(user_ids, 1):
        profile = fetch_roblox_profile(user_id)
        if profile:
            username = profile["name"]
            display_name = profile.get("displayName", username)  # use display name if available
            description = profile.get("description", "")  # use get to handle cases where description might be missing
            user_score, flag_reasons = calculate_user_score(display_name, username, description)
            flagged = user_score > 200
            percentage = min((user_score / 200) * 100, 100)
            flag_text = f"{user_score} (FLAGGED)" if flagged else str(user_score)
            if flagged:
                print(f"\033[91m{display_name} (@{username}): {user_score}/200, {percentage:.0f}% ({count}/{total_users})\033[0m")
            else:
                print(f"{display_name} (@{username}): {user_score}/200, {percentage:.0f}% ({count}/{total_users})")
            results.append((display_name, username, user_score, flagged, flag_reasons))
        time.sleep(0.15)
    return results

def sort_and_log_results(results):
    custom_flagged = sorted([result for result in results if result[3] and result[4]], key=lambda x: -x[2])
    normal_flagged = sorted([result for result in results if result[3] and not result[4]], key=lambda x: -x[2])
    non_flagged = sorted([result for result in results if not result[3]], key=lambda x: -x[2])

    sorted_results = custom_flagged + normal_flagged + non_flagged
    
    output_file = os.path.join(script_dir, "output.txt")
    with open(output_file, "w", encoding="utf-8") as file:
        for count, (display_name, username, user_score, flagged, flag_reasons) in enumerate(sorted_results, 1):
            flag_text = " [FLAGGED]" if flagged else ""
            if flagged and flag_reasons:
                reason_text = " REASON: " + "; ".join(flag_reasons)
                file.write(f"{display_name} (@{username}): {user_score}{flag_text}! {reason_text}\n")
            else:
                file.write(f"{display_name} (@{username}): {user_score}{flag_text}\n")

    print(f"Results written to {output_file}")

def main():
    group_id = input("Enter group ID that you'd like to scan: ").strip()
    user_ids = fetch_group_members(group_id)
    results = analyze_profiles(user_ids)
    sort_and_log_results(results)

if __name__ == "__main__":
    main()

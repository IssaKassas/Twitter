import json
import os
import pandas as pd
import re
from langdetect import detect as lang

def get_pattern_match(pattern, text):
    matches = re.findall(pattern, text)
    if matches:
        return matches
    
class Tweet:
    def __init__(self, username, nickname, date, post: str):
        self.username = username
        self.nickname = nickname
        self.date = date
        self.tweet = post
        self.hashtags = "#"
        self.language_code = ""

    def createJson(self):
        # Extracting hashtags using regular expressions
        hashtagsList = get_pattern_match(r'#\w+', self.tweet)
        if hashtagsList:
            self.hashtags = " ".join(hashtagsList)
            for hashtag in hashtagsList:
                self.tweet = self.tweet.replace(hashtag, "")

            self.language_code = lang(self.tweet)
        
        else:
            self.hashtags = ""
            self.language_code = lang(self.tweet)

        data = {
            "username": self.username,
            "nickname": self.nickname,
            "tweet": self.tweet,
            "date": self.date,
            "hashtags": self.hashtags,
            "language": self.language_code
        }
        
        # Get the absolute path to the current directory
        current_directory = os.getcwd()

        # Define the directory path where you want to save the JSON file
        directory_path = os.path.join(current_directory, "Json")

        # Create the directory if it doesn't exist
        if not os.path.exists(directory_path):
            os.makedirs(directory_path)

        file_path = os.path.join(directory_path, f"{self.username}.json")

        # If the file already exists, read its content first
        existing_data = []
        if os.path.exists(file_path):
            with open(file_path, 'r') as json_file:
                existing_data = json.load(json_file)

        # Append the new tweet data to the existing data
        existing_data.append(data)

        # Write the combined data to the JSON file
        with open(file_path, 'w') as json_file:
            json.dump(existing_data, json_file, indent=4)
        
        return file_path

    def createDataset(self, jsonfile):
    # Load the JSON data
        with open(jsonfile) as json_file:
            data = json.load(json_file)

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame to CSV file
        df.to_csv('Dataset.csv', index=False)

def createDataset(jsonfile):
    # Load the JSON data
        with open(jsonfile) as json_file:
            data = json.load(json_file)

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)

        # Save DataFrame to CSV file
        df.to_csv('Dataset.csv', index=False)
import os
import re
import glob
import csv

def split_transcript(file_path):
    # Getting the unique id for file names--> Ex: 1000_transcript.txt --> 1000_transcript_participant.txt & 1000_transcript_chatbot.txt
    base_name = os.path.basename(file_path)
    base_name = os.path.splitext(base_name)[0]  #removes the .txt part so we dont get "1000_transcript_participant.txt.txt"
    
     # output files go into current directory
    user_file = f"{base_name}_participant.txt"
    assistant_file = f"{base_name}_chatbot.txt"
    
    #unique ID from filename
    unique_id = base_name.split('_')[0]
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    user_messages = [] #stores "user" messages aka participant
    assistant_messages = [] #stores "assistant" messages aka chatbot
    
    #for csv
    all_messages = []
    turn_number = 1
    
    # Process each line individually for more precise classification
    current_message = "" # empty string for current message
    current_type = None # to figure out "who" is speaking --> "user" or "assistant"
    current_content = ""
    
    for line in lines:
        user_match = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*? - user:(.*)", line) # format matching, Ex: 2025-02-19 17:18:11 UTC-05:00-0500 - user:"
        assistant_match = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}.*? - assistant:(.*)", line) # 2025-02-19 17:18:11 UTC-05:00-0500 - assistant:
        
        if user_match or assistant_match:
            if current_content and current_type:
                if current_type == "user":
                    user_messages.append(current_content.strip())
                    all_messages.append({
                        'UniqueID': unique_id,
                        'TurnNo': turn_number,
                        'Speaker': 'participant',
                        'Text': current_content.strip()
                    })
                elif current_type == "assistant":
                    assistant_messages.append(current_content.strip())
                    all_messages.append({
                        'UniqueID': unique_id,
                        'TurnNo': turn_number,
                        'Speaker': 'chatbot',
                        'Text': current_content.strip()
                    })
                turn_number += 1
            
            if user_match:
                current_type = "user"
                current_message = line.strip()
                current_content = user_match.group(1).strip()
            elif assistant_match:
                current_type = "assistant"
                current_message = line.strip()
                current_content = assistant_match.group(1).strip()
        else:
            if current_message: 
                current_message += "\n" + line.strip()
                current_content += "\n" + line.strip()
    
    if current_content and current_type:
        if current_type == "user":
            user_messages.append(current_content.strip())
            all_messages.append({
                'UniqueID': unique_id,
                'TurnNo': turn_number,
                'Speaker': 'participant',
                'Text': current_content.strip()
            })
        elif current_type == "assistant":
            assistant_messages.append(current_content.strip())
            all_messages.append({
                'UniqueID': unique_id,
                'TurnNo': turn_number,
                'Speaker': 'chatbot',
                'Text': current_content.strip()
            })
    
    with open(user_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(user_messages))
    
    with open(assistant_file, 'w', encoding='utf-8') as f:
        f.write('\n\n'.join(assistant_messages))
    
    return all_messages

def create_csv_from_transcripts(transcript_files, output_csv='transcript_turns.csv'):
    all_turns = []
    
    for file_path in transcript_files:
        try:
            turns = split_transcript(file_path)
            all_turns.extend(turns)
        except Exception as e:
            print(f"Error processing {file_path}: {str(e)}")
    
    #sorting by UniqueID and turns
    all_turns.sort(key=lambda x: (x['UniqueID'], x['TurnNo']))
    if all_turns:
        with open(output_csv, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['UniqueID', 'TurnNo', 'Speaker', 'Text']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(all_turns)
        return True
    return False

def main():
    txt_files = glob.glob("*.txt") #getting all .txt files
    transcript_files = [f for f in txt_files if not (f.endswith("_participant.txt") or f.endswith("_chatbot.txt"))]
    
    if transcript_files:
        csv_created = create_csv_from_transcripts(transcript_files)
        
        if csv_created:
            print("Transcripts processed successfully. CSV file created with all speaking turns of all trascripst located in this directory.")
        else:
            print("No transcripts found to create the CSV file.")
    else:
        print("No transcript files found in the current directory.")

if __name__ == "__main__":
    main()
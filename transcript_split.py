from pathlib import Path
import re

def read_file(sourcefile, all_output):
    stem_of_file = Path(sourcefile).stem #gets me the "1001_transcript"
    unique_ID = re.sub(r"_transcript", "", stem_of_file) #replaces "_transcript" with empty string so we extract the actual ID

    with open(sourcefile, "r") as f, open(f"participant_{unique_ID}.txt", "w") as participant, open(f"chatbot_{unique_ID}.txt", "w") as chatbot:
        turn_no = 1 #turn number starts at 1
        for line in f: #looping through each line of file
            if line.strip(): #check if line is not empty
                participant_line = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC-\d{2}:\d{2}-\d{4} - user: (.*)", line.strip()) #pattern match to the line that belongs to participant
                if participant_line: #if participant line is found
                    print(participant_line.group(1), file = participant) #for creating individual files 
                    print(f'{unique_ID},{turn_no},participant,"{participant_line.group(1)}"', file=all_output) #putting data into the columns of csv
                    turn_no += 1 #increment turn number
                    continue #put continue so that chatbot line is not processed in this iteration, we expect only one "person" per line, if we have a case where chatbot and particpant talk on same line, remove this continue statement
                chatbot_line = re.match(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} UTC-\d{2}:\d{2}-\d{4} - assistant: (.*)", line.strip()) #pattern match to the line that belongs to chatbot
                if chatbot_line: #if chatbot line is found
                    print(chatbot_line.group(1), file = chatbot) #for creating individual files, putting just the text of chatbot, no metadata
                    print(f'{unique_ID},{turn_no},chatbot,"{chatbot_line.group(1)}"', file=all_output) #putting data into the columns of csv
                    turn_no += 1 #increment turn number
                    continue

if __name__ == "__main__":
    with open("all_output.csv", "w") as all_output:  # Open the output file
        all_output.write("UniqueID,TurnNo,Speaker,Text\n") #the columns in csv file puts new line after columns created
        for files in Path(".").glob("*.txt"): #every file in the current directory with .txt extension
            read_file(files, all_output) # call the read_file function for each file
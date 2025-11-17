# Automated Transcript Splitter
## Developed for Department of Media and Information at MSU in College of Communication Arts and Sciences(Chatbot Experiment)
### All transcripts (.txt files) are read in, processed into the "person" speaking whether that is participant or chatbot. Based on categorization, responses get separated into their own text files with the content of the message. After all scripts are processed a csv file is created with 4 columns (UniqueID, Turn Number, Speaker, Text). Turn number resets with each new source transcript file being read in.

Reworked original script to one just under 30 lines with a single function doing most of the work. This code is more straightforward, uses pre-built methods or libraries where needed to do most of the heavy lifting. There's a comment on each line to understand what the code is doing and tweak for different cases.

Last updated: 8/6/2025

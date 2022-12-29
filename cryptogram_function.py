import string; import random; import re; import sys
def make_cryptogram(entry):
    """TAKES AN ENTRY FROM A TEXT FILE AS INPUT AND TURNS IT INTO A SIMPLE SUBSTITUTION CODE
    CRYPTOGRAM LIKE WHAT APPEARS IN PENNY DELL PUZZLE BOOKS. EACH LETTER IN THE
    ENTRY IS CODED AS A DIFFERENT LETTER. A NEW CODE IS GENERATED FOR EACH ENTRY -
    ALL APPEARS AS UPPERCASE."""
    u_case_list = list(string.ascii_uppercase)
    entry_string = ""
    crypto_dict = {}; crypto_list = []
    entry = entry.lower()

    for letter in entry:
        if letter in string.digits: # reset everything if we encounter a number (indicates a new entry).
            u_case_list = list(string.ascii_uppercase)
            output_list = []
            crypto_dict = {}
        if not re.search("[a-zA-Z0-9!?,.-:;'() \n]",letter): # can't use \w token b/c of underscore
            print("Input needs to be proofread. Contains unrecognized character")
            sys.exit(0)
        if letter in crypto_dict:
            continue # skip letter - it's been encountered already in current entry
        if letter in string.ascii_lowercase:
            chosen = random.choice(u_case_list)
            if letter == chosen.lower(): # in case letter chosen is the same letter
                u_case_list.remove(chosen)
                crypto_dict[letter] = random.choice(u_case_list) # ensures non-matching letter is paired
                u_case_list.append(chosen) # returns letter to list in case all 26 are needed
                continue
            u_case_list.remove(chosen)
            crypto_dict[letter] = chosen

        else: # keeps all numbers and punctuation the same
            crypto_dict[letter] = letter

    for char in entry:
        entry_string = entry_string + (crypto_dict[char])

    return entry_string

while True:
    final_string = ''
    input_attempt = input("Please supply the file name for making cryptograms or enter 'Quit' to exit:\n")
    if re.search("(\s)*(Q|q)uit(\s)*",input_attempt): sys.exit(0)
    try:
        input_crypto = open(input_attempt).read()
        break
    except:
        print("File name not recognized. Please try again or enter 'Quit' to exit")
        continue
ic_copy = input_crypto.lower() # to preserve original

format_phrase = "(\d{1,2}\.\s[a-zA-Z!?,.-:;'() ]+\n\n)+\d{1,2}\.\s[a-zA-Z!?,.-:;'() ]+"
if not re.search(format_phrase,ic_copy): # format check for whole document
    print("Document is not in proper format. Please revise and try again")
    sys.exit(0)

num_list = re.findall("[0-9]{1,2}(?=\.)",ic_copy) # make list of numbers preceding periods
num_list = [int(num) for num in num_list] # turn strings into numbers

if num_list != list(range(1,(len(num_list)+1))): # check that all numbers are consecutive
    print("Formatting error. Numbers need to be consecutive. Proofread and try again please.")
    sys.exit(0)

entries_list = []    # find beginning pos using i\. find end_pos using next number
for i in range(1,len(num_list)+1):
    if i < max(num_list):
        beg_pos = ic_copy.find(str(i))
        end_pos = ic_copy.find(str(i+1))
        entries_list.append(ic_copy[beg_pos:end_pos])

    else: # for last entry which ends with single \n.
        beg_pos = ic_copy.find(str(i))
        end_pos = ic_copy.find("\n",beg_pos)
        entries_list.append(ic_copy[beg_pos:end_pos])

for entry in entries_list: # combine all entries into one string
    f = make_cryptogram(entry)
    final_string = final_string + f

print(final_string)

file_out = open("crypto_output.txt","w") # to working directory
file_out.write(final_string)
file_out.close()

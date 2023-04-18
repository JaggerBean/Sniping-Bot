with open('player_futbin_data.txt', 'r') as f_in, open('player_futbin_data2.txt', 'w') as f_out:
    # Loop through the lines of the input file
    for i, line in enumerate(f_in):
        # Skip the 3rd line by checking if the line number modulo 3 is 0
        if (i + 1) % 3 != 0:
            # Write the line to the output file
            f_out.write(line)

with open('player_futbin_data2.txt', 'r') as f:
    lines = f.readlines()

for i in range(1, len(lines), 2):
    lines[i-1] = lines[i-1].rstrip() + '/' + lines[i]

output = ''.join(lines)

with open('player_futbin_data2.txt', 'w') as f:
    f.write(output)


# Open the original file and read its lines into a list
with open('player_futbin_data2.txt', 'r') as f:
    lines = f.readlines()

# Create a new list of lines containing only the odd-indexed lines
new_lines = []
for i, line in enumerate(lines):
    if i % 2 == 0:
        new_lines.append(line)

# Open the file again in write mode and write the new lines to it
with open('player_futbin_data2.txt', 'w') as f:
    f.writelines(new_lines)

import pandas as pd

# Read the text document into a list
with open('player_futbin_data2.txt', 'r') as f:
    lines = f.readlines()

# Extract the necessary information
data = []
player_id = ''
player_name = ''
card_type = ''
counter = 0
for line in lines:
    counter += 1
    line = line.strip()
    parts = line.split('/')
    player_id = parts[-3]
    player_name = parts[-2]
    card_type = parts[-1]
    if len(card_type) < 2:
        print(counter)
    data.append([player_id, player_name, card_type])

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['ID', 'Player Name', 'Card Type'])

# Save the DataFrame to an Excel file
df.to_excel('player_futbin_data.xlsx', index=False)

# Create a DataFrame from the extracted data
df = pd.DataFrame(data, columns=['ID', 'Player Name', 'Card Type'])

# Save the DataFrame to an Excel file
df.to_excel('player_futbin_data.xlsx', index=False)
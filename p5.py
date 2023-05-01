from bs4 import BeautifulSoup

# Open the HTML file
with open("/home/esrom/Desktop/web/index.html", "r") as file:
    # Load the file into BeautifulSoup
    soup = BeautifulSoup(file, "html.parser")

# Prompt the user for a word to insert
word = input("Enter a word to insert: ")

# Create a new paragraph element with the word
new_paragraph = soup.new_tag("p")
new_paragraph.string = word

# Append the new paragraph element to the HTML body
body = soup.body
body.append(new_paragraph)

# Save the modified HTML file
with open("/home/esrom/Desktop/web/index.html", "w") as file:
    file.write(str(soup))

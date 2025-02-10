def modify_word(word):
    # List of words that should output "huzz"
    special_words = ["girls", "girl", "female", "women"]
    
    # Check if the word is in the special list
    if word.lower() in special_words:
        return "huzz"
    
    # For all other words, replace the last letter with "uzz"
    return word[:-1] + "uzz"

# Get input from the huzz
input_word = input("Enter a word: ")

# Modify the word and print the result
result = modify_word(input_word)
print(f"Huzz word: {result}")
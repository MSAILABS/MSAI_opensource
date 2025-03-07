def remove_non_alphanumeric(input_string: str) -> str: 
    # Create a new string with only alphanumeric characters 
    cleaned_string = ''.join(char for char in input_string if char.isalnum())

    if (len(cleaned_string) > 200):
        cleaned_string = cleaned_string[:200]
    else:
        return cleaned_string
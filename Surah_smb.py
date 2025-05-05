import json
import re

def get_symbol(name, existing_symbols):
    """Generates a unique symbol for a surah, ensuring correct letter order and sentence case."""

    first_letter = name[0].upper()
    remaining_consonants = re.findall(r"[^aeiouAEIOU\s]", name[1:])
    vowels = re.findall(r"[aeiouAEIOU]", name[1:])

    if len(remaining_consonants) >= 2:
        symbol = first_letter + remaining_consonants[0].lower() + remaining_consonants[1].lower()
    elif len(remaining_consonants) == 1:
        symbol = first_letter + remaining_consonants[0].lower()
    else:
        symbol = first_letter

    # Check and correct letter order
    symbol_letters = re.findall(r"[^0-9]", symbol)
    name_consonants = [name[0].upper()] + re.findall(r"[^aeiouAEIOU\s]", name[1:].lower())

    if len(symbol_letters) > 1:
        if name_consonants[0].upper() != symbol_letters[0].upper() or name_consonants[1].lower() != symbol_letters[1].lower() or (len(symbol_letters) > 2 and name_consonants[2].lower() != symbol_letters[2].lower()):
            # Correct the order and case
            symbol = name_consonants[0].upper() + "".join(name_consonants[1:len(symbol_letters)]).lower()

    if symbol not in existing_symbols:
        return symbol

    # Try replacing the last consonant with a later one
    if len(remaining_consonants) > 2:
        symbol = first_letter + remaining_consonants[0].lower() + remaining_consonants[2].lower()
        if symbol not in existing_symbols:
            return symbol

    # Try using vowels if all consonant combinations fail
    if vowels and remaining_consonants:
        vowel_index = name[1:].lower().find(vowels[0].lower())
        consonant_index = name[1:].lower().find(remaining_consonants[0].lower())

        if vowel_index < consonant_index:
            symbol = first_letter + vowels[0].lower() + remaining_consonants[0].lower()
        else:
            symbol = first_letter + remaining_consonants[0].lower() + vowels[0].lower()
        if symbol not in existing_symbols:
            return symbol

    # If everything fails, add a number to the symbol
    i = 1
    while True:
        new_symbol = symbol + str(i)
        if new_symbol not in existing_symbols:
            return new_symbol
        i += 1
    return symbol

# Load surah data from JSON
with open("surah.json", "r") as f:
    surah_data = json.load(f)

# Sort surahs by order in reverse
surah_data.sort(key=lambda x: x["order"], reverse=True)

# Generate and add symbols
existing_symbols = set()
for surah in surah_data:
    symbol = get_symbol(surah["name"], existing_symbols)
    surah["Symbol"] = symbol
    existing_symbols.add(symbol)
    print(f"Symbol for {surah['name']}: {symbol}")

# Sort surahs back by order
surah_data.sort(key=lambda x: x["order"])

# Save modified data to surah_mod.json
with open("surah_mod.json", "w") as f:
    json.dump(surah_data, f, indent=4)

print("surah_mod.json created with Symbol attributes.")
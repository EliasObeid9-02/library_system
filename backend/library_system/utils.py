def capitalize_sentence(sentence: str):
    words = sentence.split(" ")
    return " ".join([word.capitalize() for word in words])


def get_order(edition_number: int):
    if edition_number % 10 == 1:
        suffix = "st"
    elif edition_number % 10 == 2:
        suffix = "nd"
    elif edition_number % 10 == 3:
        suffix = "rd"
    else:
        suffix = "th"
    return f"{edition_number}{suffix}"

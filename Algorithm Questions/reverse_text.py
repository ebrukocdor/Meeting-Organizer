def reverse_text(input_text):
    result = []
    words = input_text.split()

    for word in words:
        # Check if word is inside parentheses, meaning it's already correct
        if word.startswith("(") and word.endswith(")"):
            result.append(word[1:-1])  # Remove the parentheses
        else:
            # Reverse the word and append
            result.append(word[::-1])

    return " ".join(result)


input_text = "nhoJ (Griffith) nodnoL saw (an) (American) ,tsilevon ,tsilanruoj (and) laicos .tsivitca ((A) reenoip (of) laicremmoc noitcif (and) naciremA ,senizagam (he) saw eno (of) (the) tsrif (American) srohtua (to) emoceb (an) lanoitanretni ytirbelec (and) nrae a egral enutrof (from) ).gnitirw"
correct_answer = "John Griffith London was an American novelist, journalist, and social activist. (A pioneer of commercial fiction and American magazines, he was one of the first American authors to become an international celebrity and earn a large fortune from writing.)"

print("Correct !!!" if reverse_text(input_text) == correct_answer else "Wrong answer...!")

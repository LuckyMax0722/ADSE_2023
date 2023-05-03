"""
Goal of Task 1:
    Implement a function that reverses the word order of a string.
"""


def reverse(sentence):
    """
    input:
        sentence (type: str)

    output:
        reversed_sentence (type: str)
    """

    # Task:
    # ToDo: Compute the reversed word order of a string.
    #       The usage of python packages is not allowed for this task.
    ########################
    #  Start of your code  #
    ########################
    sentence = sentence + " "
    word_extra = ""
    reversed_sentence = ""

    n = 0

    while n < len(sentence):
        if sentence[n] == " ":
            reversed_sentence = " " + word_extra + reversed_sentence
            word_extra = ""
        else:
            word_extra = word_extra + sentence[n]

        n = n + 1

    list_str = list(reversed_sentence)
    list_str.pop(0)
    reversed_sentence = ''.join(list_str)
    ########################
    #   End of your code   #
    ########################

    return reversed_sentence


if __name__ == "__main__":
    assert reverse("this is a test") == "test a is this"

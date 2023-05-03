"""
Goal of Task 0:
    Implement a function that calculates the factorial of a number.
"""


def factorial(n):
    """
    input:
        n (type: int): given number

    output:
        fact (type: int): factorial of the number
    """

    # Task:
    # ToDo: Calculate the factorial of a given number. No python packages are allowed.
    # Hints:
    #   - e.g. for 6 the function should return 720.
    #   - consider recursive implementation
    ########################
    #  Start of your code  #
    ########################
    fact = 1

    while n > 0:
        fact = fact * n
        n = n - 1
    ########################
    #   End of your code   #
    ########################

    return fact


if __name__ == "__main__":
    assert factorial(6) == 720

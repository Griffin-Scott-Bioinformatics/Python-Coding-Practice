#!/usr/bin/env python
# reverse_a_string
""" Simple practice reversing a string using different methods
and timing them."""
import time
import string
import random
import matplotlib.pyplot as plt
import sys


def _tic():
    """ Function to record start time
    :return:
    """
    return time.perf_counter()


def _toc():
    """ Function to record stop time
    :return:
    """
    return time.perf_counter()


def _outstatement(method, rev, time_start, time_stop, is_random):
    """ General purpose out statement function
    :param method: method of reversing (ie function calling this one)
    :param rev: reversed sequence
    :param time_start:
    :param time_stop:
    :param is_random: Boolean
    :return:
    """
    # Because the randomly generated input is long and nonsense
    # we don't want to print the entire string just the performance

    if is_random:
        print(f'Reversed using {method}\nThis method took {time_stop - time_start} seconds.')
        print('-------------------------------------------')
    else:
        print(f'Reversed using {method}\n{rev}\nThis method took {time_stop - time_start} seconds.')
        print('-------------------------------------------')


def _get_histogram_data(length, method, time_start, time_stop, timeout='N'):
    performance = time_stop - time_start
    hist_list.append((length, method, performance, timeout))


def _recursion_loop(in_string):
    """ Created a helper function simply to avoid recurrently passing the
    unnecessary is_random argument to the reversing portion of the code.
    :param in_string:
    :return:
    """
    if in_string == '':
        return in_string
    else:
        return _recursion_loop(in_string[1:]) + in_string[0]


def brak_reverse(in_string, is_random):
    """ Reverse the string using the typical comprehension method
    :param in_string: verified user input string
    :param is_random: true or false check for randomly generated input
    :return: prints output information
    """

    start = _tic()
    rev_string = in_string[::-1]
    if from_input:
        _outstatement('a split', rev_string, start, _toc(), is_random)
    else:
        _get_histogram_data(len(in_string), 'Split', start, _toc())


def loop_reverse(in_string, is_random):
    """ Less efficient loop method to demonstrate the utility of timing
    :param in_string: same input or random string
    :param in_string:
    :param is_random:
    """

    start = _tic()
    lrev_string = ""
    for i in in_string:
        lrev_string = i + lrev_string

    if from_input:
        _outstatement('a for-loop', lrev_string, start, _toc(), is_random)
    else:
        _get_histogram_data(len(in_string), 'Loop', start, _toc())


def using_recursion(in_string, is_random):
    """ Method using a recursive function, this method
    will crash the program if used on a string that is greater than
    around 1500 characters, therefore it is skipped for longer strings.
    :param in_string:
    :param is_random:
    :return:
    """

    start = _tic()

    # Recursions create memory issues if they are too deep,
    # this logic skips the recursion method if the string is too long
    if len(in_string) < 1500:
        if from_input:
            _outstatement('recursion', _recursion_loop(in_string), start, _toc(), is_random)
        else:
            _get_histogram_data(len(in_string), 'Recursion', start, _toc())
    else:
        if from_input:
            print('String is too long, recursion will run out of memory')
        else:
            _get_histogram_data(len(in_string), 'Recursion', start, _toc(), timeout="Y")


def using_method(in_string, is_random):
    """ Using the built-in reversed method to create and then join
    a reversed list of the characters.
    :param in_string:
    :param is_random:
    :return:
    """
    start = _tic()
    reversed_string = "".join(reversed(in_string))
    if from_input:
        _outstatement('.reversed() method', reversed_string, start, _toc(), is_random)
    else:
        _get_histogram_data(len(in_string), 'Method', start, _toc())


def using_comprehension(in_string, is_random):
    """ Method using a stupidly complicated list comprehension.
    The kind of thing you write when you first learn about comprehensions.
    :param in_string:
    :param is_random:
    :return:
    """
    start = _tic()
    rev_string = "".join([in_string[i] for i in range(len(in_string)-1, -1, -1)])

    if from_input:
        _outstatement('Using a really dumb comprehension',
                      rev_string, start, _toc(), is_random)
    else:
        _get_histogram_data(len(in_string), 'Comprehension', start, _toc())


def run_reverses(in_string, random_n=1000):
    # In order to test the performance of different methods a very long string will be randomly generated
    # and passed to the functions
    is_random = False
    if in_string == '':
        in_string = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random_n))
        is_random = True

    brak_reverse(in_string, is_random)
    loop_reverse(in_string, is_random)
    using_recursion(in_string, is_random)
    using_method(in_string, is_random)
    using_comprehension(in_string, is_random)


#def generate_bar_charts(dictionary):


def generate_histogram_values():
    histionary = {}
    for i in range(0, 110000, 10000):
        run_reverses('', i)

    list_of_pairs = []
    for hist_set in hist_list:
        for j in hist_list:
            if j[0] is hist_set[0]:
                list_of_pairs.append((j[1], j[2] if j[3] == "N" else 0))

        histionary[hist_set[0]] = list_of_pairs
        if len(list_of_pairs) == 5:
            list_of_pairs = []

   # generate_bar_charts(histionary)
    for key, item in histionary.items():

        # Save labels and parameters for each loop
        title = key
        method = list(zip(*item))[0]
        performance = list(zip(*item))[1]

        # Normalizing performance to better compare charts
        performance_normalized =  [float(i)/sum(performance) for i in performance]
        plt.figure()
        plt.title(title)
        plt.ylim(0,1)
        plt.bar(method, performance_normalized)
        plt.show()


def main():
    global from_input
    from_input = True

    please = "Please write a string to reverse or press enter to generate a new string of 1000 characters:"
    run_reverses(input(please))

    # WARNING this is the current tolerated limit, mess with this value at your own risk
    sys.setrecursionlimit(1500)

    global hist_list
    hist_list = []

    hist_input = input('Would you like to generate a time histogram? y/n')
    if hist_input.casefold() == 'yes' or hist_input == 'y':
        from_input = False
        generate_histogram_values()


if __name__ == '__main__':
    main()

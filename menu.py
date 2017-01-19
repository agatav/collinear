# -*- coding: utf-8 -*-
import sys
from datetime import datetime
import brute_force as brute
from random import randint


# coordinates generator
def gen_coordinates(m, n):
    seen = set()
    x = randint(m, n)
    while True:
        seen.add(x)
        yield (x)
        x = randint(m, n)
        while x in seen:
            x = randint(m, n)


def get_numeric():
    while True:
        try:
            res = float(input('How many points would you like to enter? '))
            break
        except (ValueError, NameError):
            print("Numbers only please!")
    return res


def main():
    quest = "Would you like to test program manually?"

    def query_yes_no(question, default="yes"):
        valid = {"yes": True, "y": True, "ye": True,
                 "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = raw_input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                 "(or 'y' or 'n').\n")

    if query_yes_no(quest, default="yes"):
        test_points = set([])
        k = get_numeric()
        i=1
        while i < k+1:
            try:
                x = input('Enter point[%i] x coordinate: ' % i)
                y = input('Enter point[%i] y coordinate: ' % i)
                i = i+1
                test_points.add(brute.Point(x, y))
            except (ValueError, NameError):
                print("Numbers only please!")
        print (test_points)

        start_time1 = datetime.now()
        print ('The amount of possible solutions with brute-force function: %i ' %
               brute.final_result_brute(test_points).points)
        print (datetime.now() - start_time1)
        print ('How many lines you need to win: %i' % brute.final_result_brute(test_points).depth)

        start_time2 = datetime.now()
        print ('The amount of possible solutions with modified brute-force function: %i ' %
               brute.final_result_faster_brute(test_points).points)
        print (datetime.now() - start_time2)
        print ('How many lines you need to win: %i' % brute.final_result_brute(test_points).depth)

    else:
        k = int(get_numeric())
        g = gen_coordinates(0, 100)
        i = 0
        while i < 10:
            i = i + 1
            test_points = set([])
            for n in range(0, k):
                test_points.add(brute.Point(next(g), next(g)))
            if brute.final_result_brute(test_points).points == brute.final_result_faster_brute(test_points).points:
                print("Test is passed")
            else:
                print("Test is not passed")

if __name__ == "__main__":
    main()
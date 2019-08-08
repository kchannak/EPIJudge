import collections
import functools

from test_framework import generic_test
from test_framework.test_failure import TestFailure
from test_framework.test_utils import enable_executor_hook


def even_odd(A):
    even, odd = 0, len(A)-1
    while even < odd:
        # Skip to the odd number for the even index
        while even < odd and A[even] % 2 == 0:
            even += 1
        while even < odd and A[odd] % 2 != 0:
            odd -= 1
        if even < odd:
            A[even], A[odd] = A[odd], A[even]
            even, odd =  even + 1, odd - 1
    return


@enable_executor_hook
def even_odd_wrapper(executor, A):
    before = collections.Counter(A)

    executor.run(functools.partial(even_odd, A))

    in_odd = False
    for a in A:
        if a % 2 == 0:
            if in_odd:
                raise TestFailure("Even elements appear in odd part")
        else:
            in_odd = True
    after = collections.Counter(A)
    if before != after:
        raise TestFailure("Elements mismatch")


if __name__ == '__main__':
    exit(
        generic_test.generic_test_main("even_odd_array.py",
                                       'even_odd_array.tsv', even_odd_wrapper))

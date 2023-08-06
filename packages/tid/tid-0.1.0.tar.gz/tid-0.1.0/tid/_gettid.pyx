cdef extern from "<sys/syscall.h>" nogil:
    int __NR_gettid
    long syscall(long number, ...)


def say_hello_to(name):
    """Example documentation.
    """
    print('Hello %s!' % name)


def gettid():
    """Get the LWP id as visible in top/ps.
    """
    return syscall(__NR_gettid)

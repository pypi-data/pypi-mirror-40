import modelx as mx
import pytest


# tree levels: 0, 1
# base counts: 0, 1


def foo():
    return 2310

def fibo(x):
    return fibo(x-1) + fibo(x-2) if x > 1 else x

def distance(x, y):
    return (x ** 2 + y ** 2) ** 0.5


def first_params(n):
    return None

def second_params(m):
    return None

def third_prams(o):
    return None


def first_params_multbases(n):
    return None

def second_params_multbases(m):
    return None

def third_params_multbases(o):
    return None


@pytest.fixture
def single_level_space():
    space = mx.new_space()
    space.set_formula(formula=first_params)


@pytest.fixture
def mult_level_space():
    space = mx.new_space()
    space.set_formula(formula=first_params)
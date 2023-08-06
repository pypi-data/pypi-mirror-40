from modelx import *

m = new_model()
s = m.new_space()

@defcells
def a(t=None):
    t = t if not t is None else 0
    return t

a()
m.save('test.mx')

test_model = open_model('test.mx', 'test')
test_model.Space1.a(1)


# PRE = [100,1,100,2,85,1,1,0] # string
PRE = [100,1,100,1,100,1,100,1] # int
PRE = [100,2,100,2,100,2,100,2] # string
import dis

def f():
    a=1
    b=1
    c=1
    d=1
    e=1
    f=1
    g=1
    h=1
    i=1
    j=1
    k=1
    l=1
    m=1
    n=1
    o=1
    p=1
    q=1
    r=1
    s=1
    t=1
    u=1
    v=1
    w=1
    x=1
    y=1
    z=1
    print('end')

END = [116, 0, 100, 2, 131, 1, 1, 0, 100, 1, 83, 0]
import sys
k = [int(sys.argv[1]), int(sys.argv[2])]
v = f.__code__.replace(co_code=bytes(PRE + k + END))
#print(dis.dis(v))
try:
    import dis
    bytecode = dis.Bytecode(f)
    exec(v)
except TypeError:
    pass
except AttributeError:
    pass
except ImportError:
    pass
except NameError:
    pass
except UnboundLocalError:
    pass
except ValueError:
    pass
except SystemError:
    sys.exit(0)
with open('tokens.py', 'a') as f:
    f.write('[' + ','.join([sys.argv[1], sys.argv[2]]) + '],' + '\n')

sys.exit(0)

#import marshal
#marshal.dump(f.__code__, open('f.dump', 'wb+'))
#code = marshal.load(open('test.dump'))
#f.__code__ == code

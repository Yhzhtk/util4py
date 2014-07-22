# coding=utf-8

def calc_base(base):
    '''calculate the numbers meet the base conditions, l1 and l2 is sorted, then merge sort without repeat'''

    # 0 special
    if base == 0:
        ll = [i * 10 for i in range(1, 11)]
        return ll

    # contain base
    l1 = []
    bsingle = base
    bten = base * 10
    for i in range(1, 10):
        bsingle += 10
        if i != base:
            l1.append(bsingle)
        else:
            l1.extend([bten + j for j in range(10)])
    
    # multiple
    l2 = []
    t = 100 / base + 1
    bmulti = 0
    for i in range(1, t):
        # no use multiplication, use addition for efficient
        bmulti += base
        l2.append(bmulti)
    
    # merge sort, not repeat
    ll = []
    while l1 and l2:
        if l1[0] < l2[0]:
            ll.append(l1.pop(0))
        elif l1[0] > l2[0]:
            ll.append(l2.pop(0))
        else:
            # for not repeat
            l2.pop(0)
    return ll + l1 + l2

def match_condition(n, ll, say, result):
    '''judge whether match the list'''
    for l in ll:
        if n == l:
            result[0] = True
            result[1] = result[1] + say
            break
        elif n < l:
            # because ll is sorted so it can break
            break
    return result

def test_calc():
    '''test the calc_base method'''
    for i in range(10):
        print i, len(calc_base(i))
        print calc_base(i)
        print

if __name__ == '__main__':
    '''I calculate the list by addition rather than use for i in range 100 by division,
     I think the addition is more efficient than division even thought it's like more complex'''
    
    n1 = int(raw_input("Input the first single digits:"))
    n2 = int(raw_input("Input the second single digits:"))
    n3 = int(raw_input("Input the third single digits:"))
    lf = calc_base(n1)
    lb = calc_base(n2)
    lw = calc_base(n3)
    for n in xrange(1, 101):
        result = [False, '']
        match_condition(n, lf, 'Fizz', result)
        match_condition(n, lb, 'Buzz', result)
        match_condition(n, lw, 'Whizz', result)
        if result[0]:
            print result[1]
        else:
            print n

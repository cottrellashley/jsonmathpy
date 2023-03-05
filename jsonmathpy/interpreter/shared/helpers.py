import re

def match_tensors(i):
    string = i
    rank = string.count('_') + string.count('^')
    if rank > 0:
        pattern = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\=[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        pattern2 = lambda x : "([a-zA-Z]+)([_^]\{[a-zA-Z]+\}|[_^]\{[a-zA-Z]+\:[0-9]}){" + str(x) + "}(?=(\*|\)|\+|\-|\/|$))"
        Total = re.match(pattern(rank), string)
        Total2 = re.match(pattern2(rank), string)
        return bool(Total) or bool(Total2)
    else:
        return False

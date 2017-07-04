__author__ = 'changpzh'

def lines(file):
    for line in file:
        yield line
    yield "\n"

def blocks(file):
    block = []
    for line in lines(file):
        '''
        收集遇到的所有行，直到遇到空行，然后返回已收集的行，
        返回的行就是一个块。
        '''
        if line.strip():
            block.append(line)
        elif block:
            yield ''.join(block).strip()
            block = []
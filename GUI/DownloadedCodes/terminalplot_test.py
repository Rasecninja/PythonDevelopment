from terminalplot import plot
from terminalplot import get_terminal_size
x = range(100)
y = [i for i in x]
plot(x, y)
print(get_terminal_size())
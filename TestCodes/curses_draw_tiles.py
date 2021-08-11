import curses

screen = curses.initscr()
num_rows, num_cols = screen.getmaxyx()

for i in range(num_cols-1):
    for j in range(num_rows-1):
        if(i%2):
            if(j%2): screen.addch(j,i,0x00002588)
        else:
            if(not j%2): screen.addch(j,i,0x00002588)

screen.refresh()

c=screen.getch()
print("Max col:",num_cols)
print("Max row:",num_rows)

curses.endwin()





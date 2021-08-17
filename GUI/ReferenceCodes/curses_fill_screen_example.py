import curses

screen = curses.initscr()
num_rows, num_cols = screen.getmaxyx()


############# Fill the screen with colors ####################
# curses.start_color()
# curses.use_default_colors()
# curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
# curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)
# while True:

#     for i in range(num_cols-1):
#         for j in range(num_rows-1):
#             if(i%2):
#                 if(j%2): 
#                     screen.addch(j,i,0x00002588,curses.color_pair(1)) #Char for full block

#             else:
#                 if(not j%2): 
#                     screen.addch(j,i,0x00002588,curses.color_pair(2))

#     screen.refresh()
#     curses.napms(100)
#     screen.clear()
#     screen.refresh()
#     curses.napms(100)



########### Fill the screen with monochrome ##################
# while True:

#     for i in range(num_cols-1):
#         for j in range(num_rows-1):
#             if(i%2):
#                 if(j%2): 
#                     screen.addch(j,i,0x00002588) #Char for full block

#             else:
#                 if(not j%2): 
#                     screen.addch(j,i,0x00002588)

#     screen.refresh()
#     curses.napms(30)
#     screen.clear()
#     screen.refresh()
#     curses.napms(30)




curses.start_color()
curses.use_default_colors()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_GREEN)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_GREEN)

for i in range(num_cols-1):
    for j in range(num_rows-1):
        if(i%2):
            if(j%2): 
                screen.addch(j,i,0x00002588,curses.color_pair(1)) #Char for full block

        else:
            if(not j%2): 
                screen.addch(j,i,0x00002588,curses.color_pair(2))

screen.refresh()

c=screen.getch()
print("Max col:",num_cols)
print("Max row:",num_rows)
print("Has colors:",curses.has_colors())

curses.endwin()





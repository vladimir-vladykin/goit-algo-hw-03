import turtle

def main():
    # figure out what order of snowflake we have to use
    print("Welcome to Koch Snowflake rendering program")
    raw_order = input("Enter how many iteration you'd like to run for snowflake (number non less than zero and not bigger than 100) >>>   ")

    
    # validation
    if not raw_order.isdigit():
        print("Cannot execute rendering, no valid number of iterations provided")
        return
    
    order = int(raw_order)
    if order < 0 or order > 100:
        print("Cannot execute rendering, number iterations should be not less than zero and no bigger than 100")
        return


    # draw snowflake
    draw_koch_snowflake(order)


# draw snowflake via drawing 3 koch curves
def draw_koch_snowflake(order, size=300):
    # prepare rendering
    window = turtle.Screen()
    window.bgcolor("white")

    t = turtle.Turtle()
    t.speed(0)  
    t.penup()
    t.goto(-size / 2, 0)
    t.pendown()


    # render snowflake.
    # koch snowflake is basically 3 koch curves, 
    # built around triangle, so draw 3 curves, but at different angle

    # first part of snowflake.
    # turn our direction on 60 degree, so instead of drawing 
    # left-to-right, we're draw from bottom-left to top-right, 
    # basically we're going from bottom left point of triangle 
    # to top point
    t.left(60)
    koch_curve(t, order, size)

    # second part of snowflake.
    # turn direction from top point to bottom right point
    t.right(120)
    koch_curve(t, order, size)

    # last part of snowflake.
    # turn direction to close our triangle, 
    # go from bottom right to bottom left, which completes our snowflake
    t.right(120)
    koch_curve(t, order, size)

    window.mainloop()

# draws single koch curve
def koch_curve(t, order, size):
    if order == 0:
        t.forward(size)
    else:
        for angle in [60, -120, 60, 0]:
            koch_curve(t, order - 1, size / 3)
            t.left(angle)


if __name__ == "__main__":
    main()
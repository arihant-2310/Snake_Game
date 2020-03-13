import turtle
import time
import random
import pygame
import itertools
import threading
import sys


#Loading animation 
done = False
#here is the animation
def animate():
    for c in itertools.cycle(['|', '/', '-', '\\']):
        if done:
            break
        sys.stdout.write('\rloading ' + c)
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write('\rDone!     ')

t = threading.Thread(target=animate)
t.start()

#long process here
time.sleep(3)
done = True

pygame.mixer.init()

pygame.mixer.music.load("The Perfect Snake Game.mp3")

pygame.mixer.music.play()

delay = 0.1  

# Score
score = 0
high_score = 0

#set up the screen
wn = turtle.Screen()
wn.title("Snake Game By @AJ2310")
wn.bgcolor("green")
wn.setup(width=600, height=600)
wn.tracer(0) #keep the animation off on the screen / turns off screen updates

#snake head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("black")
head.penup()
head.goto(0,0)
head.direction = "stop"

#Snake Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0,100)

segments = []

# Pen
pen = turtle.Turtle()
pen.speed(0)
pen.shape("square")
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0,260)
pen.write("Score: 0 High Score: 0", align="center", font=("Courier", 24, "normal"))


#Functions
def go_up():
	if head.direction != "down":
		head.direction = "up"

def go_down():
	if head.direction != "up":
		head.direction = "down"

def go_right():
	if head.direction != "left":
		head.direction = "right"

def go_left():
	if head.direction != "right":
		head.direction = "left"

def move():
	if head.direction == "up":
		y = head.ycor()
		head.sety(y + 20)

	if head.direction == "down":
		y = head.ycor()
		head.sety(y - 20)

	if head.direction == "left":
		x = head.xcor()
		head.setx(x - 20)

	if head.direction == "right":
		x = head.xcor()
		head.setx(x + 20)
#Keyboard Bindings

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_right, "Right")
wn.onkeypress(go_left, "Left")

#main game loop
while True:
	wn.update()

	#Check for collision with the border
	if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
		time.sleep(1)
		head.goto(0,0)
		head.direction = "stop"
		pygame.mixer.music.load("shoot.wav")
		pygame.mixer.music.play()

		#Hide the segments
		for segment in segments:
			segment.goto(1000,1000)

		#Clear the segment list
		segments.clear()

		#Reset The Score
		score =0

		#Reset the delay
		delay = 0.1

		pen.clear()
		pen.write("Score: {} High Score: {}".format(score,high_score), align="center", font= ("Courier", 24, "normal"))



	#Check with the collison for the food
	if head.distance(food) < 20:
		#Move the food to random spot
		x = random.randint(-290, 290)
		y = random.randint(-290, 290)
		food.goto(x,y)

		#Add a segment
		new_segment = turtle.Turtle()
		new_segment.speed(0) #animation speed
		new_segment.shape("square")
		new_segment.color("grey")
		new_segment.penup()
		segments.append(new_segment)

		#Shorten the delay
		delay -= 0.001

		#Increase the score
		score += 10

		if score > high_score:
			high_score = score
		pen.clear()
		pen.write("Score: {} High Score: {}".format(score,high_score), align="center", font= ("Courier", 24, "normal"))

	#Move the end segments first in reverse order
	for index in range(len(segments)-1, 0, -1):
		x = segments[index-1].xcor()
		y = segments[index-1].ycor()
		segments[index].goto(x,y)

	#Move segments 0 to where the head is
	if len(segments) > 0:
		x = head.xcor()
		y = head.ycor()
		segments[0].goto(x,y)


	move()

	#Check for head collison with the body segments
	for segment in segments:
		if segment.distance(head) < 20:
			time.sleep(1)
			head.goto(0,0)
			head.direction = "stop"
			pygame.mixer.music.load("pause.mp3")
			pygame.mixer.music.play()

			#Hide the segments
			for segment in segments:
				segment.goto(1000,1000)

			#Clear the segment list
			segments.clear()

			#Reset The Score
			score =0

			#Reset the delay
			delay = 0.1

			#Update the score display
			pen.clear()
			pen.write("Score: {} High Score: {}".format(score,high_score), align="center", font= ("Courier", 24, "normal"))


	time.sleep(delay)

wn.mainloop() #keep the window on for us
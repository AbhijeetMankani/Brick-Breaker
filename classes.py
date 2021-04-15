# Predefined Canvas Width and Height values
c_height = 600 
c_width = 963


class Brick:
	def __init__(self, _col, _row, _present, leftX, topY, canvas):
		self.col = _col
		self.row = _row

		self.width = 80
		self.height = 20
		self.present = _present
		self.id=canvas.create_rectangle(leftX, topY, leftX + self.width, topY + self.height, fill='#0000FF')
	
	def delete(self, canvas):
		'''Deletes the brick'''
		if(self.present):
			canvas.delete(self.id)
			self.present=0
		

		
class Paddle:
	def __init__(self, _x, canvas):
		self.x = _x
		self.y = c_height - 20
		
		self.width = 100
		self.height = 10
		
		self.id=canvas.create_rectangle(self.x-self.width/2, self.y - self.height/2, self.x + self.width/2, self.y + self.height/2, fill='#FFFFFF')
	
	def movement(self, canvas, mov_x, mov_y):
		'''To move the paddle'''
		canvas.move(self.id, mov_x, mov_y)
		self.x+=mov_x
		self.y+=mov_y

class Ball:
	def __init__(self, _x, _y, _speedX, _speedY, canvas):
		self.x = _x
		self.y = _y

		self.r = 10
	
		self.speedX = _speedX
		self.speedY = _speedY

		self.max_speed = 20
		self.min_speed = 5

		self.id = canvas.create_oval(self.x - self.r, self.y - self.r, self.x + self.r, self.y + self.r, fill='#FFFFFF')

	def movement(self, canvas, mov_x, mov_y):
		'''To move the ball'''
		canvas.move(self.id, mov_x, mov_y)
		self.x+=mov_x
		self.y+=mov_y
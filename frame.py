import random

import pygame

import constant as c

s_width = c.s_width
s_height = c.s_height
play_width = c.play_width
play_height = c.play_height
block_size = c.block_size

top_left_x = (s_width - play_width)//2
top_left_y = s_height - play_height

score_dic = {0:5 , 1:100 , 2:200 , 3:400 , 4:800}
shapes = c.shapes
shape_colors = [(0,255,0),(255,0,0),(0,255,255),(255,255,0),(0,0,255),(255,165,0),(128,0,128)]


class piece(object):
      rows = 20
      columns = 10 

      def __init__(self,column,row,shape):
            self.x = column
            self.y = row
            self.shape = shape
            self.color = shape_colors[shapes.index(shape)]
            self.rotation = 0
            self.index = shapes.index(shape)

def create_grid(locked_pos = {}):
      grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

      for i in range(len(grid)):
            for j in range(len(grid[i])):
                  if (j,i) in locked_pos:
                        c = locked_pos[(j,i)]
                        grid[i][j] = c

      return grid

def get_shape():
      # global shapes, shape_colors
      
      return piece(5,0,random.choice(shapes))

def convert_shape_format(shape):
      positions = []
      format = shape.shape[shape.rotation % len(shape.shape)]

      for i , line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                  if column == '0':
                        positions.append((shape.x + j, shape.y + i))

      for i , pos in enumerate(positions):
            positions[i] = (pos[0] - 2, pos[1] - 4)

      return positions


def valid_space(shape, grid):
      accepted_pos = [[(j,i) for j in range(10)if grid[i][j] == (0,0,0)]for i in range(20)]
      accepted_pos = [j for sub in accepted_pos for j in sub]
      # print(accepted_pos)

      formatted = convert_shape_format(shape)

      for pos in formatted:
            if pos not in accepted_pos:
                  if pos[1] > -1 or pos[0] >= 10 or pos[0] < 0:
                        # print('alert')
                        return False
      return True



def check_lost(positions):
      for pos in positions:
            x, y = pos
            if y < 1:
                  
                  return True
      
      return False

def current_group():
      pool = [i for i in range(7)]

      a = random.sample(pool, 7)

      return a




def get_shapes():

      group = []
      for x in current_group():
            one_shape = piece(5,0,shapes[x])
            group.append(one_shape)


      
      return group


def index_shapes(index):

      index = index% 7
      

      return index




def draw_gird(surface,grid):
      sx = top_left_x
      sy = top_left_y

      for i in range(len(grid)):
            pygame.draw.line(surface,(128,128,128), (sx,sy + i *block_size),(sx+play_width,sy + i*block_size))
            for j in range(len(grid[i])):
                  pygame.draw.line(surface,(128,128,128), (sx + j *block_size,sy ),(sx + j*block_size, sy + play_height))


      
def clear_rows(grid, locked):
      inc = 0
      ind  = []
      for i in range(len(grid)-1,-1,-1):
            row = grid[i]
            if (0,0,0) not in row:
                  inc += 1
                  ind.append(i)
                  for j in range(len(row)):
                        try:
                              del locked[(j,i)]
                        except:
                              continue
      if inc > 0:
            for i in range(len(ind)):
                  for key in sorted(list(locked), key = lambda x: x[1])[::-1]:
                        x, y = key                        
                        if y < ind[i]+i:
                              newKey =(x,y + 1)
                              locked[newKey] = locked.pop(key)

      return inc
                  

def draw_pieces(number,format,surface,color,x,y):
      block_size_ =block_size*0.9
      for a in range(number):
            
            for i, line in enumerate(format):
                  row = list(line)
                  for j, column in enumerate(row):
                        if column == '0':
                              pygame.draw.rect(surface, color, (x + j*block_size_, y+ i*block_size_,block_size_,block_size_), 0)
                              pygame.draw.line(surface,(128,128,128), (x+ j*block_size_ ,y+ i*block_size_ ),(x+ j*block_size_ + block_size_, y+ i*block_size_  ))
                              pygame.draw.line(surface,(128,128,128), (x+ j*block_size_ ,y+ i*block_size_ ),(x+ j*block_size_ , y+ i*block_size_+ block_size_  ))

            y += 100


def draw_next_shapes(group, next_group, surface, number , next_index):
      font = pygame.font.SysFont('comicsans', 20)
      label = font.render('Next Shape', 1, (255,255,255))

      sx = top_left_x + play_width + 50
      sy = top_left_y + play_height/2 - 300

      y = sy

      # shape_list = []
      for i in range(number):
            shape = group[next_index]
            format = shape.shape[shape.rotation % len(shape.shape)]
            draw_pieces(1,format,surface,shape.color,sx , y )
            y += 110

            next_index += 1
            if next_index == 7:
                  group = next_group
                  next_index = 0    
             

      
      # format = shape.shape[shape.rotation % len(shape.shape)]

      # draw_pieces(number,format,surface,shape.color,sx , sy )

      # for i, line in enumerate(format):
      #       row = list(line)
      #       for j, column in enumerate(row):
      #             if column == '0':
      #                   pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size,block_size,block_size), 0)

      surface.blit(label, (sx + 10, sy - 30))

def draw_hold_piece(surface, hold_piece):

      # pass
      font = pygame.font.SysFont('comicsans', 20)
      label = font.render('Hold', 1, (255,255,255))

      sx = top_left_x - play_width/2 - 50
      sy = top_left_y + play_height/2

      
      
      if hold_piece!= 0:

            shape = hold_piece

            format = shape.shape[shape.rotation % len(shape.shape)]

            draw_pieces(1,format,surface,shape.color,sx , sy ) 

      surface.blit(label, (sx , sy - 30))


      
      # if hold_piece == 0:
      #       hold_piece = current_piece
      #       current_ = next_piece





def draw_score(surface,score,last_score):

      # score = clear_rows(grid, locked)
      
      font = pygame.font.SysFont('comicsans', 20)
      label = font.render('Score:'+str(score), 1, (255,255,255))

      surface.blit(label,(top_left_x - play_width - 50 + play_width/2,30))

      font = pygame.font.SysFont('comicsans', 20)
      label1 = font.render('High Score:'+str(last_score), 1, (255,255,255))

      surface.blit(label1,(top_left_x - play_width - 50 + play_width/2,60))




def draw_middle_text(surface, text, size, color):

      font = pygame.font.SysFont('comicsans', size, bold = True)
      label = font.render(text, 1, color)

      surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2), top_left_y + play_height/2 - (label.get_height()/2)))


def update_score(nscore):
      score = max_score()

      with open('score.txt', 'w') as f:
            f.write(str(max(int(score),nscore)))
                  

def max_score():
      try:
            with open('score.txt', 'r') as f:
                  lines = f.readlines()
                  score = lines[0].strip()
                  # print(score)
      except:
            score = 0

      return score     

def draw_predict(locked,position,grid):
      
      record =[]
      position_ = []
      for a in position:
            temp = []
            for c in a:
                  temp.append(c)
            position_.append(temp)

      # print(position_)
      for i in range(len(position_)):
            x,y = position_[i][0],position[i][1]
            while (x,y) not in locked and y < 20:
                  y += 1
                  
            y -= 1
           
            record.append(y - position[i][1])
            
      down = min(record)
      for i in range(len(position_)):
                  x, y = position_[i][0] ,position[i][1]+down
                  # print(x,y)
                  if y > -1 and y < 20 and x >= 0 and x < 10:
                        grid[y][x] = (70,70,70,240)

def draw_window(surface,grid):

      surface.fill((0,0,0))

      font = pygame.font.SysFont('comicsans',60)
      label = font.render('Tetris',1,(255,255,255))

      surface.blit(label,(top_left_x + play_width/2 - (label.get_width()/2),25))

      for i in range(len(grid)):
            for j in range(len(grid[i])):
                  pygame.draw.rect(surface,grid[i][j],(top_left_x + j*30, top_left_y + i*30,30,30),0)

      pygame.draw.rect(surface,(255,0,0),(top_left_x, top_left_y, play_width, play_height),4)

      

      draw_gird(surface,grid)
      # pygame.display.update()

# print(get_shapes()[0])



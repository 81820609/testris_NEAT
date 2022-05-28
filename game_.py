import pygame
from attr import s

import constant as c
from frame import *

pygame.init()

class gameinformation:
    def __int__(self, score):
        self.score = score


class Game_tetris:
    # s_width = c.s_width
    # s_height = c.s_height    

    def __init__(self,window):
        self.win = window
        self.s_width = 800
        self.s_height = 700
        self.locked_positions = {}
        self.grid = create_grid(self.locked_positions)

        self.change_piece = False
        self.hold_state = False
        self.event_count = 0
        
        self.current_group = get_shapes()
        self.next_group = get_shapes()
        self.shapes_index = 0
        self.shape_pos = []
        self.next_index = 1
        self.current_piece = self.current_group[self.shapes_index]
        self.next_piece = self.current_group[self.next_index]
        self.hold_piece = 0
        self.holdone = True
        
        # clock = pygame.time.Clock()
        self.hole = 0
        self.height = 0
        self.high_column = [0]*10
        self.hole = [0]*10
        self.dif = [0]*10
        # self.max_high = 0
        self.min_high = 0
        self.line = 0
        self.all_line = 0
        self.score_dic = c.score_dic
        self.score = 0
        self.current_score = 0
        self.delay_time = 0
        self.time_delay = 200
        self.fall_time = 0
        self.fall_speed = 0
        # current_speed = fall_speed
        self.level_time = 0
        self.last_score = max_score()
        self.level = 0
        self.move_time = 0
        self.move_speed = 0.03
        self.long_press = {'down':False,'left':False,'right':False}
        self.wait_motion = False
        self.finishe_motion = False
        self.wait_time = 0
        self.motion_count = 0
        self.human = False
        

    def fall(self,time):
        self.fall_time += time
        self.level_time += time
        if self.level_time/1000 >= 10:
                  level_time = 0
                  if self.fall_speed > 0.15:
                        self.fall_speed -= self.level


        if self.fall_time/1000 >= self.fall_speed:
                self.fall_time = 0                  
                self.current_piece.y += 1
                if not(valid_space(self.current_piece, self.grid)) and self.current_piece.y > 0:
                    self.current_piece.y -= 1
                    if self.human and not self.finishe_motion:
                        self.wait_motion = True 
                        
                    print('alert1')
                    if not self.wait_motion:                        
                        self.change_piece = True
                        self.finishe_motion = False

    def move_state(self,event):
          
                        
        if event == 'left':
            self.long_press['left'] = True           

            self.current_piece.x -= 1
            if not(valid_space(self.current_piece,self.grid)):
                self.current_piece.x += 1

        if event == 'right':
            self.long_press['right'] = True
            self.current_piece.x += 1
            if not(valid_space(self.current_piece,self.grid)):
                self.current_piece.x -= 1
                
        
        if event == 'down':
            self.long_press['down'] = True
            self.current_piece.y += 1
            if not(valid_space(self.current_piece,self.grid)):
                self.current_piece.y -= 1

        if event == 'rotation_clock':
            self.current_piece.rotation += 1
            
            if not(valid_space(self.current_piece,self.grid)):
                if not self.super_rotation():
                    self.current_piece.rotation -= 1

        if event == 'rotation_cnclock':
            self.current_piece.rotation -= 1
            
            if not(valid_space(self.current_piece,self.grid)):
                if not self.super_rotation():
                    self.current_piece.rotation += 1

        if event == 'down_imd':
            self.current_piece.y += 1
            while valid_space(self.current_piece, self.grid) and self.current_piece.y > 0:
                self.current_piece.y += 1
            self.current_piece.y -= 1
            self.change_piece = True
            
        if event == 'hold':
            if self.hold_piece == 0 :
                self.hold_piece = self.current_piece
                self.change_piece = True
                self.hold_state = True
                
               
                
            else:                
                self.hold_piece, self.current_piece = self.current_piece, self.hold_piece
                self.current_piece.x, self.current_piece.y = 5,0
                   
                    
                    
        
        if event == 'left_kup':
                self.long_press['left'] = False
                self.delay_time = 0
                

        if event == 'right_kup':
                self.long_press['right'] = False
                self.delay_time = 0

        if event == 'down_kup':
                self.long_press['down'] = False
                self.delay_time = 0

    def longpress(self,time):
        for state in self.long_press:
            if self.long_press[state]:                
                self.move_time += time
                self.delay_time += time
                if self.delay_time >= self.time_delay:
                        if self.move_time/1000 >= self.move_speed:
                            self.move_time = 0
                            if state == 'left':
                                self.current_piece.x -= 1
                                if not(valid_space(self.current_piece,self.grid)):
                                        self.current_piece.x += 1

                            if state == 'right':
                                self.current_piece.x += 1
                                if not(valid_space(self.current_piece,self.grid)):
                                        self.current_piece.x -= 1

                            if state == 'down':
                                self.current_piece.y += 1
                                if not(valid_space(self.current_piece,self.grid)):
                                        self.current_piece.y -= 1

    def super_rotation(self,rot = True):
        ind_s =self.current_piece.index
        if rot:
            ind_r = self.current_piece.rotation + 1
        # else:
        #     ind_r = self.current_piece.rotation - 1
        ind_r = ind_r %4
        # dic_i = None

        if ind_s ==3:
            dic_i = 'O'
        elif ind_s == 2:
            dic_i = 'I'
        else:
            dic_i = 'Other'

        
        for x in c.SRS_dic[dic_i][ind_r]:
            self.current_piece.x += x[0]
            self.current_piece.y += x[1]
            if not(valid_space(self.current_piece,self.grid)):
                self.current_piece.x -= x[0]
                self.current_piece.y -= x[1]                
            else:
                return True
        return False

    
    def detect(self):
        hole = [0]*10
        
        
        # height = 0
        for i in range(20):
            for j in range(10):
                if self.grid[i][j] !=(0,0,0):
                    if i < 19:
                        if self.grid[i+1][j] == (0,0,0):
                            hole[j] += 1
                    self.height = max(self.height, 20-i)
                    self.high_column[j] = max(self.high_column[j], 20-i)
        # hole_net = hole - self.hole
        self.hole = hole
        for i in range(1,10):
            self.dif[i] = self.high_column[i] - self.high_column[i-1]

        self.min_high = min(self.high_column)

    def detect_new(grid):
        hole = [0]*10
        high_column = [0]*10
        dif = [0]*10
        

        
        clear_row =[]
        for i in range(20):
            for j in range(10):
                k = 1
                if grid[i][j] !=(0,0,0) and j not in clear_row:
                    while i + k < 20:
                        if grid[i+k][j] == (0,0,0):
                            hole[j] += 1
                        k += 1
                    clear_row.append(j)
                    # height = max(height, 20-i)
                    high_column[j] = max(high_column[j], 20-i)
        # hole_net = hole - self.hole
        
        for i in range(1,10):
            dif[i] = abs(high_column[i] - high_column[i-1])


        min_high = min(high_column)
        max_high = max(high_column)
        max_hole = sum(hole)
        max_dif = sum(dif)
        # print(hole)
        

        

        return max_hole,max_dif,max_high,min_high
        # return high_column,hole,dif,max_high,min_high

        

    def pre_detect(piece,grid,locked,next_state = False,piece2 = 0,pre_i = -1, pre_j = -1):
        pre_list = []
        current_list = []
        
        win2 = 0
        for i in range(10):
            
            for j in range(4):
                newgame = Game_tetris(win2)
                newgame.current_piece.shape = piece.shape
                newgame.grid = list(grid)
                newgame.locked_positions = dict(locked)
                pre_piece = newgame.current_piece
                pre_grid = newgame.grid
                pre_locked = newgame.locked_positions
                pre_piece.x = i
                pre_piece.rotation = j % len(pre_piece.shape)
                if valid_space(pre_piece, pre_grid):
                    if pre_piece.y < 0 :
                        pre_piece.y += 3
                    while valid_space(pre_piece, pre_grid) :
                        pre_piece.y += 1
                    pre_piece.y -= 1
                    pre_pos = convert_shape_format(pre_piece)
                    for pos in pre_pos:
                        p = (pos[0],pos[1])
                        pre_locked[p] = piece.color
                    pre_grid = create_grid(pre_locked)
                    line = clear_rows(pre_grid,pre_locked)
                    pre_grid = create_grid(pre_locked)
                    
                    if next_state:
                        next_list = Game_tetris.pre_detect(piece2,pre_grid,pre_locked,pre_i = i, pre_j = j)
                        pre_list.append(next_list)
                        

                    else:
                        
                        # high_column,hole,dif,max_high,min_high = Game_tetris.detect_new(pre_grid)
                        max_hole,max_dif,max_high,min_high = Game_tetris.detect_new(pre_grid)
                        # current_list += high_column + hole + dif + [max_high] + [min_high] +[line]
                        current_list +=  [max_hole]+[max_dif]+ [max_high] + [min_high] +[line]
                        if pre_i != -1 and pre_j != -1:
                            current_list += [pre_i,pre_j]
                        else:
                            current_list += [i,j]
                        pre_list.append(current_list)
                        # print(pre_pos)
                        current_list = []

        return pre_list


    def test(piece):
        piece.y += 1
        


    
    def change(self):
        if self.change_piece:
            if self.hold_state == False:
                for pos in self.shape_pos:
                    p = (pos[0],pos[1])
                    self.locked_positions[p] = self.current_piece.color           

            self.hold_state = False
            
            self.grid = create_grid(self.locked_positions)

            self.shapes_index = self.next_index
            self.next_index += 1
            if self.next_index == 7:
                self.current_group = self.next_group
                self.next_group = get_shapes()
            
            self.next_index = self.next_index % 7
            
            # print(next_index)
            self.current_piece = self.next_piece
            self.next_piece = self.current_group[self.next_index]
            self.change_piece = False
            self.line = clear_rows(self.grid, self.locked_positions)
            self.grid = create_grid(self.locked_positions)
            self.detect()
            # self.grid = create_grid(self.locked_positions)
            self.all_line += self.line
            self.current_score = self.score_dic[self.line]
            self.score += self.current_score
            return True

            
        
        
        


    def draw(self):
        # self.shape_pos = convert_shape_format(self.current_piece)
        draw_predict(self.locked_positions,self.shape_pos,self.grid)
        for i in range(len(self.shape_pos)):
                  x, y = self.shape_pos[i]
                  if y > -1:
                        self.grid[y][x] = self.current_piece.color

        # self.change()        
        draw_window(self.win,self.grid)
        draw_next_shapes(self.current_group,self.next_group,self.win,5,self.next_index)
        draw_hold_piece(self.win, self.hold_piece)
        draw_score(self.win,self.score,self.last_score)

    def lost(self):
        if check_lost(self.locked_positions):
            draw_middle_text(self.win, 'You Lost!', 60, (255,255,255))
            
            update_score(self.score)

    def reset(self):
        self.score = 0
        self.locked_positions ={}
        self.grid = create_grid(self.locked_positions)
        self.height = 0
        self.high_column = [0]*10


    def loop(self,time):
        self.grid = create_grid(self.locked_positions)
        # print(self.locked_positions)
        self.fall(time)
        
        
        
        # print(self.current_piece.y)
        self.shape_pos = convert_shape_format(self.current_piece)
        

        change = self.change()
        if check_lost(self.locked_positions):
            # draw_middle_text(self.win, 'You Lost!', 60, (255,255,255))
            
            update_score(self.score)
        game_information = self.score

        return game_information, check_lost(self.locked_positions), change, self.current_score




            




        
                            
                






import os
import pickle
import random
import time

import neat
import pygame

import constant as c
from game_ import Game_tetris

# from curses import window

shape_list = c.shapes


class tetris_game:

    def __init__(self, window):
        self.game = Game_tetris(window)
        self.current_piece = self.game.current_piece
        self.locked_positions = self.game.locked_positions
        self.next_piece = self.game.next_piece


    def player(self):

        clock = pygame.time.Clock()
        self.game.fall_speed = 0.3        
        
        run = True
        while run:
            clock.tick(60)
            time1 = clock.get_rawtime()
            game_info,lost,change,current_score = self.game.loop(time1)
            
            if lost:
                self.game.reset()
            
            for event in pygame.event.get():

                
               
                if event.type == pygame.QUIT:
                    
                    run = False
                    pygame.display.quit()
                    SystemExit 
                
                if event.type == pygame.KEYDOWN:
                        
                    if event.key == pygame.K_LEFT:
                        self.game.move_state('left')

                    if event.key == pygame.K_RIGHT:
                        self.game.move_state('right')                           
                    
                    if event.key == pygame.K_DOWN:
                        self.game.move_state('down')                        

                    if event.key == pygame.K_UP:
                        self.game.move_state('rotation_clock')                        

                    if event.key == pygame.K_z:
                        self.game.move_state( 'rotation_cnclock')                        

                    if event.key == pygame.K_SPACE:
                        self.game.move_state('down_imd')
                        
                    if event.key == pygame.K_c:
                        self.game.move_state('hold')

                if event.type == pygame.KEYUP:

                    if event.key == pygame.K_LEFT:
                        self.game.move_state('left_kup')
                        

                    if event.key == pygame.K_RIGHT:
                        self.game.move_state('right_kup')

                    if event.key == pygame.K_DOWN:
                        self.game.move_state('down_kup')
           
            self.game.draw()

            time2 = clock.get_rawtime()
            self.game.longpress(time2)
            
            pygame.display.update()
    

    def test_ai(self, winner_net):
        run = True       
        clock = pygame.time.Clock()
        net = winner_net
        action = True
        
        self.game.fall_speed = 0

        max_score = 5000

        while run:
            time4 = clock.get_rawtime()            
            game_info, lost,change,current_score = self.game.loop(time4)
            if change:
                action = True
            
            if lost :
                print(self.game.score)
                               
                self.game.reset()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            if action:
                self.AI_move(net)
                action = False

            
            
            self.game.draw()
            
            pygame.display.update()

            

    

    def AI_train(self, gen, config, draw=False):

        run = True
        
        start_time = time.time()
        clock = pygame.time.Clock()

        net = neat.nn.FeedForwardNetwork.create(gen, config)
        
        self.gen = gen
        self.game.fall_speed = 0
        action = True

        max_score = 10000000

        while run:
            time4 = clock.get_rawtime()
            # clock.tick(10)            
            game_info, lost,change,current_score = self.game.loop(time4)
            # print(self.game.current_piece.x)
            if change:
                action = True
            
            if lost or self.game.score > max_score:
                # self.game.draw()
                self.calculate_fitness(game_info, duration,current_score)                
                self.game.reset()
                break
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return True
            
            if action:
                self.AI_move(net)
                action = False

            
            if draw:
                self.game.draw()
            
            pygame.display.update()

            duration = time.time() - start_time
            
            
        
        return False
    

    def AI_move(self, net):
        
        output =[-99]
        output_list = []
        # action2 = [99,99]
        # x_lisy = []
         
        
        for x in Game_tetris.pre_detect(self.game.current_piece,self.game.grid,self.game.locked_positions):
            output_new = net.activate(x[:5]) 
            # output_list.append([output_new] + x[5:])
            # print(x)
            if output_new[0] >= output[0]:
                action2 = x[5:]
                output = output_new
                # x_list = x

        # print(x_list)

        # print(output_list)
        # print(output)
        # action_list = []
        # for x in output_list:
        #     if x[0] == output:
        #         action_list.append(x[1:])

        # if len(action_list) > 1:
        #     action2 = random.choice(action_list)
        # else:
        #     action2 = action_list[0]
        # print(action2)

        
        if action2 != [99,99]:
            x, rotation = action2[0], action2[1]
            

            x_move = x - self.game.current_piece.x
            rot_move = rotation - self.game.current_piece.rotation 

            for j_ in range(abs(rot_move)):
                if rot_move > 0:
                    self.game.move_state('rotation_clock')
                else:
                    self.game.move_state('rotation_cnclock')

            for i_ in range(abs(x_move)):
                if x_move > 0:
                    self.game.move_state('right')
                else:
                    self.game.move_state('left')

            self.game.move_state('down_imd')           




        

    def calculate_fitness(self,game_info, duration, current_score):
        self.gen.fitness += game_info
       


def eval_gens(gens, config):
    width,height = 800,700
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Tetris')
    

    for i ,(gem_id,gen) in enumerate(gens):
     
        gen.fitness = 0
        tetris = tetris_game(win)
        

        force_quit = tetris.AI_train(gen,config, draw = False)
        if force_quit:
            quit()


def eval_gens2(gens, config):
    width,height = 800,700
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Tetris')
    tetris = tetris_game(win)
    force_quit = tetris.AI_train2(gens,config, draw = False)
    if force_quit:
        quit()

    

    



def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('test-1_allline_relu_check_point_128')    
    
    # p = neat.Population(config)
    p.config.fitness_threshold = 10000000
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(10, filename_prefix='test-1_allline_relu_check_point_'))

    winner = p.run(eval_gens)
    with open("best/best-1.pickle", "wb") as f:
        pickle.dump(winner, f)


def test_best_network(config):
    with open("best/best-1.pickle", "rb") as f:
        winner = pickle.load(f)
    winner_net = neat.nn.FeedForwardNetwork.create(winner, config)

    width,height = 800,700
    win = pygame.display.set_mode((width,height))
    pygame.display.set_caption('Tetris')
    tetris = tetris_game(win)
    tetris.test_ai(winner_net)



local_dir = os.path.dirname(__file__)
config_path = os.path.join(local_dir, 'config1.txt')

config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction,
                        neat.DefaultSpeciesSet, neat.DefaultStagnation,
                        config_path)

# for i in range(20):

#test best work
test_best_network(config)

#run neat network
# run_neat(config)



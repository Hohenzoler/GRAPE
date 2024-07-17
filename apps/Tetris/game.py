import pygame
import random
import time
import sys
sys.setrecursionlimit(999_999_999)
class Game:
    def __init__(self, screen, x, y, level):
        self.width = 500
        self.height = 1000

        self.tile_size = 50

        self.boardwidth = self.width//self.tile_size
        self.boardheight = self.height//self.tile_size

        self.board = [[None for x in range(self.boardwidth)] for x in range(self.boardheight)]
        # for element in self.board:
        #     print(element)

        self.score = 0
        self.level = level - 1



        self.run = True

        self.lines_cleared = -(self.level+1)*10
        self.all_lines_cleared = 0

        self.current_master = None

        self.unalterd_fall_delay = 48/60

        self.move_delay = 0.05
        self.fall_delay = self.unalterd_fall_delay

        self.move_timer = 0
        self.fall_timer = 0

        self.volume = 1.5

        self.left_pressed = False
        self.right_pressed = False


        self.screen = screen

        self.x_offset = x
        self.y_offset = y

        self.options = ['O-block', 'I-block', 'J-block', 'L-block', 'S-block', 'T-block', 'Z-block']
        # self.options = ['O-block', 'O-block', 'O-block', 'O-block', 'O-block', 'O-block', 'O-block']

        self.blocks_in_que = self.options.copy()
        random.shuffle(self.blocks_in_que)
        self.colors_in_que = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in range(len(self.blocks_in_que))]

        self.objects = []

        self.change_level()

        QX = MasterController(self, self.blocks_in_que[0],
                              self.colors_in_que[0])

        self.blocks_in_que.pop(0)
        self.colors_in_que.pop(0)
        self.next = [self.blocks_in_que[0], self.colors_in_que[0]]
        self.current_master = QX

        self.old_master = self.current_master

        self.cleared_sound = pygame.mixer.Sound('apps/Tetris/music/clear.mp3')
        self.cleared_sound.set_volume(self.volume)

        self.tetris_sound = pygame.mixer.Sound('apps/Tetris/music/tetris.mp3')
        self.tetris_sound.set_volume(self.volume)

    def mainloop(self):
        if self.run:
            if self.current_master != self.old_master:
                self.fall_delay = self.unalterd_fall_delay
            self.update()
            self.render()

    def update(self):
        if self.current_master != None:
            if time.time() - self.fall_timer > self.fall_delay:
                self.current_master.update()
                self.fall_timer = time.time()

        self.clear_rows()

    def render(self):
        if self.left_pressed:
            if time.time() - self.move_timer > self.move_delay:
                self.move_left()
                self.move_timer = time.time()
        if self.right_pressed:
            if time.time() - self.move_timer > self.move_delay:
                self.move_right()
                self.move_timer = time.time()

        # for y in range(self.boardheight):
        #     for x in range(self.boardwidth):
        #         pygame.draw.rect(self.screen, (26, 26, 26), (x*self.tile_size + self.x_offset, y*self.tile_size + self.y_offset, self.tile_size, self.tile_size), 1)
        #
        # for y, row in enumerate(self.board):
        #     for x, element in enumerate(row):
        #         if element != None:
        #             pygame.draw.rect(self.screen, 'white', pygame.Rect(x * self.tile_size,
        #                                                                            y * self.tile_size,
        #                                                                            self.tile_size,
        #                                                                            self.tile_size))
        #             pygame.draw.rect(self.screen, (200, 200, 200),
        #                              pygame.Rect(x * self.tile_size,
        #                                          y * self.tile_size,
        #                                          self.tile_size, self.tile_size), 1)

        for object in self.objects:
            # print(object.blocks)
            object.render()

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_d:
                self.current_master.rotate('right')
            if event.key == pygame.K_a:
                self.current_master.rotate('left')
            if event.key == pygame.K_LEFT:
                self.left_pressed = True
            if event.key == pygame.K_RIGHT:
                self.right_pressed = True
            if event.key == pygame.K_DOWN:
                self.fall_delay = 1/60


        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.left_pressed = False
            if event.key == pygame.K_RIGHT:
                self.right_pressed = False
            if event.key == pygame.K_DOWN:
                self.fall_delay = self.unalterd_fall_delay
                self.old_master = self.current_master

    def create_block(self):
        QX = MasterController(self, self.blocks_in_que[0],
                              self.colors_in_que[0])

        self.blocks_in_que.pop(0)
        self.colors_in_que.pop(0)

        if len(self.blocks_in_que) == 0:
            self.blocks_in_que = self.options.copy()
            random.shuffle(self.blocks_in_que)
            self.colors_in_que = [(random.randint(50, 255), random.randint(50, 255), random.randint(50, 255)) for _ in
                                  range(len(self.blocks_in_que))]

        self.next = [self.blocks_in_que[0], self.colors_in_que[0]]



        self.current_master = QX

        if self.fall_delay != self.unalterd_fall_delay:
            self.old_master = None
        else:
            self.old_master = self.current_master


    def move_left(self):
        if self.current_master != None:
           self.current_master.move_left()

    def move_right(self):
        if self.current_master != None:
           self.current_master.move_right()

    def clear_rows(self):

        rows_to_delete = []
        for i in range(len(self.board) - 1, -1, -1):
            row = self.board[i]
            num_of_blocks = 0
            for element in row:
                if element != None and element.master != self.current_master:
                    num_of_blocks += 1
                else:
                    break
            if num_of_blocks == self.boardwidth:
                rows_to_delete.append(i)
                for block in self.board[i]:
                    block.master.blocks.remove(block)
                    del block
                self.board[i] = [None for x in range(self.boardwidth)]

            else:
                for block in self.board[i]:
                    if block != None:
                        block.update_after_row_deletion(len(rows_to_delete))


        if len(rows_to_delete) > 0:
            self.lines_cleared += len(rows_to_delete)
            self.all_lines_cleared += len(rows_to_delete)

            if self.lines_cleared >= 10:
                self.lines_cleared = self.lines_cleared-10
                self.change_level()

            if len(rows_to_delete) == 1:
                self.score += (40*(self.level+1))
                self.cleared_sound.play()
            elif len(rows_to_delete) == 2:
                self.score += (100 * (self.level + 1))
                self.cleared_sound.play()
            elif len(rows_to_delete) == 3:
                self.score += (300 * (self.level + 1))
                self.cleared_sound.play()
            elif len(rows_to_delete) == 4:
                self.score += (1200 * (self.level + 1))
                self.tetris_sound.play()



    def change_level(self):
        self.level += 1
        if self.level <= 29:
            if self.level <= 8:
                self.unalterd_fall_delay = (48 - self.level*5)/60
            if self.level == 9:
                self.unalterd_fall_delay = 6/60
            if self.level >= 10:
                self.unalterd_fall_delay = 5/60
            if self.level >= 13:
                self.unalterd_fall_delay = 4/60
            if self.level >= 16:
                self.unalterd_fall_delay = 3/60
            if self.level >= 19:
                self.unalterd_fall_delay = 2/60
            if self.level >= 29:
                self.unalterd_fall_delay = 1/60
            self.fall_delay = self.unalterd_fall_delay




class MasterController:
    def __init__(self, game, Type, color):
        self.game = game
        self.type = Type

        self.can_move = True
        self.can_move_left = True
        self.can_move_right = True

        self.rotation = 0

        self.color = color

        self.move_s = pygame.mixer.Sound('apps/Tetris/music/move.mp3')
        self.move_s.set_volume(self.game.volume)

        self.place_s = pygame.mixer.Sound('apps/Tetris/music/clicked_in_place.mp3')
        self.place_s.set_volume(self.game.volume)


        self.blocks = []
        self.generate_blocks()

        self.distance = self.calculate_distance_to_the_bottom()

        self.game.objects.append(self)


    def generate_blocks(self):
        if self.type == 'O-block':
            if self.game.board[1][self.game.boardwidth//2] == None and self.game.board[1][self.game.boardwidth//2 + 1] == None and  self.game.board[2][self.game.boardwidth//2] == None and self.game.board[2][self.game.boardwidth//2 + 1] == None:

                fourth_block = Blocks(self, self.game.boardwidth // 2 + 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2 + 1, 1)
                first_block = Blocks(self, self.game.boardwidth//2, 1)




        elif self.type == 'I-block':
            if self.game.board[1][self.game.boardwidth//2 - 1] == None and self.game.board[1][self.game.boardwidth//2] == None and  self.game.board[1][self.game.boardwidth//2 + 1] == None and self.game.board[1][self.game.boardwidth//2 + 2] == None:

                fourth_block = Blocks(self, self.game.boardwidth // 2 + 2, 1)
                third_block = Blocks(self, self.game.boardwidth // 2 + 1, 1)
                secound_block = Blocks(self, self.game.boardwidth // 2, 1)
                first_block = Blocks(self, self.game.boardwidth // 2 - 1, 1)

        elif self.type == 'J-block':
            if self.game.board[1][self.game.boardwidth // 2 - 1] == None and self.game.board[2][
                self.game.boardwidth // 2 - 1] == None and self.game.board[2][self.game.boardwidth // 2] == None and self.game.board[2][self.game.boardwidth // 2 + 1] == None:
                fourth_block = Blocks(self, self.game.boardwidth // 2 + 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2 - 1, 2)
                first_block = Blocks(self, self.game.boardwidth // 2 - 1, 1)


        elif self.type == 'L-block':
            if self.game.board[1][self.game.boardwidth // 2 + 1] == None and self.game.board[2][
                self.game.boardwidth // 2 - 1] == None and self.game.board[2][self.game.boardwidth // 2] == None and self.game.board[2][self.game.boardwidth // 2 + 1] == None:
                fourth_block = Blocks(self, self.game.boardwidth // 2 + 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2 - 1, 2)
                first_block = Blocks(self, self.game.boardwidth // 2 + 1, 1)



        elif self.type == 'S-block':
            if self.game.board[1][self.game.boardwidth // 2] == None and self.game.board[1][
                self.game.boardwidth // 2 + 1] == None and self.game.board[2][self.game.boardwidth // 2 - 1] == None and self.game.board[2][self.game.boardwidth // 2] == None:
                fourth_block = Blocks(self, self.game.boardwidth // 2 - 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2 + 1, 1)
                first_block = Blocks(self, self.game.boardwidth // 2, 1)


        elif self.type == 'T-block':
            if self.game.board[1][self.game.boardwidth // 2] == None and self.game.board[2][
                self.game.boardwidth // 2 - 1] == None and self.game.board[2][self.game.boardwidth // 2] == None and self.game.board[2][self.game.boardwidth // 2 + 1] == None:
                fourth_block = Blocks(self, self.game.boardwidth // 2 + 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2 - 1, 2)
                first_block = Blocks(self, self.game.boardwidth // 2, 1)


        elif self.type == 'Z-block':
            if self.game.board[1][self.game.boardwidth // 2 - 1] == None and self.game.board[1][
                self.game.boardwidth // 2] == None and self.game.board[2][self.game.boardwidth // 2] == None and self.game.board[2][self.game.boardwidth // 2 + 1] == None:
                fourth_block = Blocks(self, self.game.boardwidth // 2 + 1, 2)
                third_block = Blocks(self, self.game.boardwidth // 2, 2)
                secound_block = Blocks(self, self.game.boardwidth // 2, 1)
                first_block = Blocks(self, self.game.boardwidth // 2 - 1, 1)

        self.center_block = third_block

    def render(self):
        if len(self.blocks) > 0:
            if self.game.current_master == self:
                self.distance = self.calculate_distance_to_the_bottom()

            for block in self.blocks:
                block.render(self.distance)
        else:
            del self

    def update(self):
        if self.can_move:
            for block in self.blocks:
                if block.can_move_down() == False:
                    self.can_move = False

            if self.can_move:
                for block in self.blocks:
                    block.go_down()
            else:
                try:
                    self.game.create_block()
                    self.place_s.play()
                except:
                    self.game.run = False
                    self.game.next = None

    def move_left(self):


        self.can_move_left = True
        for block in self.blocks:
            if block.can_move_left() == False:
                self.can_move_left = False

        if self.can_move_left:
            self.blocks.reverse()
            for block in self.blocks:
                block.go_left()
            self.blocks.reverse()
            self.move_s.play()


    def move_right(self):
        self.can_move_right = True
        for block in self.blocks:
            if block.can_move_right() == False:
                self.can_move_right = False

        if self.can_move_right:
            for block in self.blocks:
                block.go_right()
            self.move_s.play()

    def calculate_distance_to_the_bottom(self):

        for block in self.blocks:
            block.distance = 0

        for x in range(self.game.boardheight):
            for block in self.blocks:
                if block.can_move_down(block.y + block.distance) == True:
                    block.distance += 1
                else:
                    break

        amount = self.blocks[0].distance
        for block in self.blocks:
            if amount > block.distance:
                amount = block.distance

        return amount

    def rotate(self, directions):
        centerx, centery = self.center_block.x, self.center_block.y
        s = False
        if self.type == 'O-block':
            s = True

        if s == False:

            for block in self.blocks:
                if directions == 'right':
                    block.temp_x = -(block.y - centery) + centerx
                    block.temp_y = block.x - centerx + centery

                if directions == 'left':
                    block.temp_x = block.y - centery + centerx
                    block.temp_y = -(block.x - centerx) + centery

                try:
                    if block.valid_temp_position() == False:
                        s = True
                        break
                except:
                    s = True

        if s == True:
            if self.type != 'O-block':
               if self.type == 'I-block':
                   srs = self.test_position(directions, 'I')
                   print(srs)
               else:
                   srs = self.test_position(directions)

               if srs != None:
                   if directions == 'right':
                       block.temp_x = -(block.y - centery) + centerx + srs[0]
                       block.temp_y = block.x - centerx + centery + srs[1]

                   if directions == 'left':
                       block.temp_x = block.y - centery + centerx + srs[0]
                       block.temp_y = -(block.x - centerx) + centery + srs[1]
                   s = False
               else:
                   s =  True


        if s == False:
            for block in self.blocks:
                if self.game.board[block.y][block.x] == block:
                    self.game.board[block.y][block.x] = None
                block.x = block.temp_x
                block.y = block.temp_y
                self.game.board[block.y][block.x] = block
            if directions == 'right':
                self.rotation += 1
                if self.rotation == 4:
                    self.rotation = 0
            else:
                self.rotation -= 1
                if self.rotation == -1:
                   self.rotation = 3

    def test_position(self, dirr, I=False):
        centerx, centery = self.center_block.x, self.center_block.y
        if I == False:
            if dirr == 'right':
                if self.rotation == 0:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 2)
                        else:
                            break

                elif self.rotation == 1:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -2)
                        else:
                            break

                elif self.rotation == 2:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 2)
                        else:
                            break

                elif self.rotation == 3:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -2)
                        else:
                            break

            elif dirr == 'left':
                if self.rotation == 0:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 2)
                        else:
                            break
                elif self.rotation == 1:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -2)
                        else:
                            break
                elif self.rotation == 2:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 2)
                        else:
                            break
                elif self.rotation == 3:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (0, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -2)
                        else:
                            break
        else:
            if dirr == 'right':
                if self.rotation == 0:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -2)
                        else:
                            break

                elif self.rotation == 1:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 0)
                        else:
                            break

                elif self.rotation == 2:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, - 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 2)
                        else:
                            break

                elif self.rotation == 3:
                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = -(block.y - centery) + centerx
                        temp_y = block.x - centerx + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, -1)
                        else:
                            break

            elif dirr == 'left':
                if self.rotation == 0:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, -2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 1)
                        else:
                            break
                elif self.rotation == 1:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 2
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (2, -1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-1, 2)
                        else:
                            break
                elif self.rotation == 2:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y + 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 2)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y - 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, -1)
                        else:
                            break
                elif self.rotation == 3:
                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, 0)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x - 2
                        block.temp_y = temp_y + 1

                        if block.valid_temp_position():
                            if idx == 3:
                                return (-2, 1)
                        else:
                            break

                    for idx, block in enumerate(self.blocks):
                        temp_x = block.y - centery + centerx
                        temp_y = -(block.x - centerx) + centery

                        block.temp_x = temp_x + 1
                        block.temp_y = temp_y - 2

                        if block.valid_temp_position():
                            if idx == 3:
                                return (1, -2)
                        else:
                            break

        return None
class Blocks:
    def __init__(self, mastercontroler, x, y):
        self.master = mastercontroler
        self.x = x
        self.y = y

        self.temp_x = 0
        self.temp_y = 0

        self.master.game.board[self.y][self.x] = self

        self.distance = 0

        self.master.blocks.append(self)

    def render(self, distance=None):
        pygame.draw.rect(self.master.game.screen, self.master.color,
                         pygame.Rect(self.x * self.master.game.tile_size + self.master.game.x_offset,
                                     self.y * self.master.game.tile_size + self.master.game.y_offset,
                                     self.master.game.tile_size, self.master.game.tile_size), border_radius=5)
        pygame.draw.rect(self.master.game.screen,
                         (self.master.color[0] * 0.25, self.master.color[1] * 0.25, self.master.color[2] * 0.25),
                         pygame.Rect(self.x * self.master.game.tile_size + self.master.game.x_offset,
                                     self.y * self.master.game.tile_size + self.master.game.y_offset,
                                     self.master.game.tile_size, self.master.game.tile_size), 1, border_radius=5)
        if distance != None and distance != 0:
            pygame.draw.rect(self.master.game.screen, 'white',
                             pygame.Rect(self.x * self.master.game.tile_size + self.master.game.x_offset, (self.y+distance) * self.master.game.tile_size + self.master.game.y_offset,
                                         self.master.game.tile_size, self.master.game.tile_size), 2, border_radius=5)

    def can_move_down(self, y=None):
        if y is None:
            y = self.y

        if y >= self.master.game.boardheight - 1:
            return False

        elif self.master.game.board[y + 1][self.x] == None or self.master.game.board[y + 1][self.x].master == self.master:
            return True

        return False

    def go_down(self):
        if self.master.game.board[self.y][self.x] == self:
            self.master.game.board[self.y][self.x] = None
        self.y += 1
        self.master.game.board[self.y][self.x] = self

    def can_move_left(self):
        if self.x > 0:
            if self.master.game.board[self.y][self.x - 1] == None or self.master.game.board[self.y][self.x - 1].master == self.master:
                return True
            else:
                return False
        return False

    def go_left(self):
        if self.master.game.board[self.y][self.x] == self:
            self.master.game.board[self.y][self.x] = None
        self.x -= 1
        self.master.game.board[self.y][self.x] = self

    def can_move_right(self):
        if self.x < self.master.game.boardwidth-1:
            if self.master.game.board[self.y][self.x + 1] == None or self.master.game.board[self.y][self.x + 1].master == self.master:
                return True
            else:
                return False
        return False

    def go_right(self):
        if self.master.game.board[self.y][self.x] == self:
            self.master.game.board[self.y][self.x] = None
        self.x += 1
        self.master.game.board[self.y][self.x] = self

    def update_after_row_deletion(self, amount):
        for x in range(amount):
            if self.master.game.board[self.y][self.x] == self:
                self.master.game.board[self.y][self.x] = None
            self.y += 1
            self.master.game.board[self.y][self.x] = self

    def valid_temp_position(self):
        if self.temp_y > self.master.game.boardheight:
            return False
        if self.temp_x >= self.master.game.boardwidth:
            return False

        if self.master.game.board[self.temp_y][self.temp_x] == None or self.master.game.board[self.temp_y][self.temp_x].master == self.master:
            if self.temp_x >= 0 and self.temp_x <= self.master.game.boardwidth and self.temp_y >= 0 and self.temp_y <= self.master.game.boardheight:
                return True
            else:
                return False
        return False


class DemoBlock:
    def __init__(self, screen, Type , color, x, y):
        self.screen = screen
        self.type = Type
        self.color = color
        self.width = 300
        self.height = 200
        self.tile_size = 43

        self.x_offset = x
        self.y_offset = y

        self.boardwidth = self.width // self.tile_size
        self.boardheight = self.height // self.tile_size

        self.blocks = []
        self.generate_demo_block()

    def generate_demo_block(self):
        if self.type == 'O-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 - 0.5, 3)
            third_block = D_Blocks(self, self.boardwidth // 2 + 0.5, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 - 0.5, 2)
            first_block = D_Blocks(self, self.boardwidth // 2 + 0.5, 2)

        elif self.type == 'I-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 + 1.5, 3)
            third_block = D_Blocks(self, self.boardwidth // 2 + 0.5, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 - 0.5, 3)
            first_block = D_Blocks(self, self.boardwidth // 2 - 1.5, 3)

        elif self.type == 'J-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 + 1, 3)
            third_block = D_Blocks(self, self.boardwidth // 2, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 - 1, 3)
            first_block = D_Blocks(self, self.boardwidth // 2 - 1, 2)


        elif self.type == 'L-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 + 1, 3)
            third_block = D_Blocks(self, self.boardwidth // 2, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 - 1, 3)
            first_block = D_Blocks(self, self.boardwidth // 2 + 1, 2)

        elif self.type == 'S-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 - 1, 3)
            third_block = D_Blocks(self, self.boardwidth // 2, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 + 1, 2)
            first_block = D_Blocks(self, self.boardwidth // 2, 2)


        elif self.type == 'T-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 + 1, 3)
            third_block = D_Blocks(self, self.boardwidth // 2, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2 - 1, 3)
            first_block = D_Blocks(self, self.boardwidth // 2, 2)


        elif self.type == 'Z-block':
            fourth_block = D_Blocks(self, self.boardwidth // 2 + 1, 3)
            third_block = D_Blocks(self, self.boardwidth // 2, 3)
            secound_block = D_Blocks(self, self.boardwidth // 2, 2)
            first_block = D_Blocks(self, self.boardwidth // 2 - 1, 2)

    def render(self):
        for b in self.blocks:
            b.render()


class D_Blocks:
    def __init__(self, mastercontroler, x, y):
        self.master = mastercontroler
        self.x = x
        self.y = y


        self.master.blocks.append(self)

    def render(self, distance=None):
        pygame.draw.rect(self.master.screen, self.master.color,
                         pygame.Rect(self.x * self.master.tile_size + self.master.x_offset,
                                     self.y * self.master.tile_size + self.master.y_offset,
                                     self.master.tile_size, self.master.tile_size), border_radius=5)
        pygame.draw.rect(self.master.screen,
                         (self.master.color[0] * 0.25, self.master.color[1] * 0.25, self.master.color[2] * 0.25),
                         pygame.Rect(self.x * self.master.tile_size + self.master.x_offset,
                                     self.y * self.master.tile_size + self.master.y_offset,
                                     self.master.tile_size, self.master.tile_size), 1, border_radius=5)

class TempObj:
    def __init__(self):
        self.score = 0
        self.level = 0
        self.run = None
        self.all_lines_cleared = 0
    def events(self, idk):
        pass

    def mainloop(self):
        pass


class LevelSelector:
    def __init__(self, screen, x, y, font):
        self.x_offset = x
        self.y_offset = y

        self.font = font

        self.screen = screen

        self.width = 400
        self.height = 160

        self.tile_size = 80

        self.selected = 0
        self.level = self.selected

        self.A_modifier = False

        self.rect = pygame.Rect(x, y, self.width, self.height)

        self.highlighted = [0, 0]

        self.matrix = [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

        self.move_s = pygame.mixer.Sound('apps/Tetris/music/move.mp3')
        self.move_s.set_volume(1.5)

        self.place_s = pygame.mixer.Sound('apps/Tetris/music/clicked_in_place.mp3')
        self.place_s.set_volume(1.5)

    def render(self):
        for y, row in enumerate(self.matrix):
            for x, element in enumerate(row):

                if self.selected == self.matrix[y][x]:
                    pygame.draw.rect(self.screen, (0, 200, 0), (
                    x * self.tile_size + self.x_offset, y * self.tile_size + self.y_offset, self.tile_size,
                    self.tile_size))

                elif self.matrix[self.highlighted[1]][self.highlighted[0]] == self.matrix[y][x]:
                    pygame.draw.rect(self.screen, (200, 200, 0), (
                    x * self.tile_size + self.x_offset, y * self.tile_size + self.y_offset, self.tile_size,
                    self.tile_size))

                pygame.draw.rect(self.screen, (26, 26, 26), (x*self.tile_size + self.x_offset, y*self.tile_size + self.y_offset, self.tile_size, self.tile_size), 5)

                number = self.font.render(str(self.matrix[y][x]), False, (255,0,0))
                number_rect = number.get_rect()
                number_rect.center = (x*self.tile_size + self.tile_size//2 + self.x_offset, y*self.tile_size + self.tile_size//2 + self.y_offset)

                self.screen.blit(number, number_rect)

    def events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                self.move('right')
            elif event.key == pygame.K_LEFT:
                self.move('left')
            elif event.key == pygame.K_DOWN:
                self.move('down')
            elif event.key == pygame.K_UP:
                self.move('up')
            elif event.key == pygame.K_a:
                self.A_modifier = True
            elif event.key == pygame.K_LSHIFT:
                self.selected = self.matrix[self.highlighted[1]][self.highlighted[0]]
                self.place_s.play()

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                self.A_modifier = False


        x, y = pygame.mouse.get_pos()

        if self.rect.collidepoint(x, y):

            self.highlighted[0], self.highlighted[1] = self.Collision(x, y)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.selected = self.matrix[self.highlighted[1]][self.highlighted[0]]
                self.place_s.play()


    def move(self, dir):

        if dir == 'right':
            if self.highlighted[0] < 4:
                self.highlighted[0] += 1
                self.move_s.play()
        elif dir == 'left':
            if self.highlighted[0] > 0:
                self.highlighted[0] -= 1
                self.move_s.play()
        elif dir == 'up':
            if self.highlighted[1] > 0:
                self.highlighted[1] -= 1
                self.move_s.play()
        elif dir == 'down':
            if self.highlighted[1] < 1:
                self.highlighted[1] += 1
                self.move_s.play()


    def Collision(self, Mx, My):
        for y, row in enumerate(self.matrix):
            for x, element in enumerate(row):
                r = pygame.Rect(x * self.tile_size + self.x_offset, y * self.tile_size + self.y_offset, self.tile_size, self.tile_size)

                if r.collidepoint(Mx, My):
                    return (x, y)

    def mainloop(self):
        self.render()
        self.update()

    def update(self):
        if self.A_modifier == False:
            self.level = self.selected
        else:
            self.level = self.selected + 10

    def reset(self):
        self.A_modifier = False




class Scoreboard:
    def __init__(self, screen, column_names, tuple_list, font_size=18, line_height=50, padding=12, max_height=300):
        self.screen = screen
        self.column_names = column_names
        self.tuple_list = tuple_list
        self.font = pygame.font.Font('apps/Tetris/font/tetris.ttf', font_size)
        self.line_height = line_height
        self.padding = padding
        self.max_height = max_height
        self.scroll_offset = 0
        self.colors = {
            "background": (20, 20, 20),
            "text": (255, 255, 255),
            "border": (26, 26, 26),
            "header_hover": (200, 200, 200)
        }
        self.column_widths = self.calculate_column_widths()
        self.sort_list(1, True)

    def calculate_column_widths(self):
        num_columns = len(self.column_names)
        max_widths = [0] * num_columns
        for tup in [self.column_names] + self.tuple_list:
            for i in range(num_columns):
                text = str(tup[i])
                text_surface = self.font.render(text, True, self.colors["text"])
                max_widths[i] = max(max_widths[i], text_surface.get_width())

        for i, width in enumerate(max_widths):
            width += 30
            max_widths[i] = width
        return max_widths

    def events(self, event):
        if event.type == pygame.MOUSEWHEEL:
            self.scroll_offset -= event.y * self.line_height
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.scroll_offset -= self.line_height
            elif event.key == pygame.K_DOWN:
                self.scroll_offset += self.line_height
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos
            if self.is_in_header(mouse_x, mouse_y):
                clicked_column = self.get_clicked_column(mouse_x)
                if clicked_column is not None:
                    self.sort_list(clicked_column, True)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            mouse_x, mouse_y = event.pos
            if self.is_in_header(mouse_x, mouse_y):
                clicked_column = self.get_clicked_column(mouse_x)
                if clicked_column is not None:
                    self.sort_list(clicked_column, False)

        self.scroll_offset = max(0, min(self.scroll_offset, self.total_height() - self.max_height + self.line_height))

    def total_height(self):
        return len(self.tuple_list) * self.line_height

    def is_in_header(self, x, y):
        header_y = (self.screen.get_height() - self.max_height) // 2
        return header_y <= y < header_y + self.line_height

    def get_clicked_column(self, x):
        xpos = (self.screen.get_width() - sum(self.column_widths) - 2 * self.padding * len(self.column_widths)) // 2
        for i, width in enumerate(self.column_widths):
            if x >= xpos and x <= xpos + width:
                return i
            xpos += width + 2 * self.padding
        return None

    def render(self):
        screen_width, screen_height = self.screen.get_size()
        menu_width = sum(self.column_widths) + 2 * self.padding * len(self.column_widths)

        x = (screen_width - menu_width) // 2
        y = (screen_height - self.max_height) // 2

        header_y = y
        xpos = x
        for i in range(len(self.column_names)):
            column_name = str(self.column_names[i])
            if column_name == str(self.column_names[self.sortby[0]]):
                if self.sortby[1] == True:
                    text_surface = self.font.render(f"{column_name} <", True, self.colors["text"])
                else:
                    text_surface = self.font.render(f"{column_name} >", True, self.colors["text"])
            else:
                text_surface = self.font.render(column_name, True, self.colors["text"])
            text_rect = text_surface.get_rect()
            column_width = self.column_widths[i]

            if self.is_in_header(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1]):
                pygame.draw.rect(
                    self.screen,
                    self.colors["header_hover"],
                    (xpos, header_y, column_width + 2 * self.padding, text_rect.height + 2 * self.padding),
                )

            pygame.draw.rect(
                self.screen,
                self.colors["background"],
                (xpos, header_y, column_width + 2 * self.padding, text_rect.height + 2 * self.padding),
            )
            pygame.draw.rect(
                self.screen,
                self.colors["border"],
                (xpos, header_y, column_width + 2 * self.padding, text_rect.height + 2 * self.padding),
                1,
            )
            self.screen.blit(
                text_surface,
                (xpos + self.padding, header_y + self.padding)
            )

            xpos += column_width + 2 * self.padding

        content_y = y + self.line_height

        clip_rect = pygame.Rect(x, content_y, menu_width, self.max_height - self.line_height)
        self.screen.set_clip(clip_rect)

        y = content_y - self.scroll_offset
        for idx, tup in enumerate(self.tuple_list):
            xpos = x
            for i in range(len(tup)):
                text = str(tup[i])
                if i == 0:
                    text_surface = self.font.render(f"{idx + 1}. {text}", True, self.colors["text"])
                else:
                    text_surface = self.font.render(text, True, self.colors["text"])
                text_rect = text_surface.get_rect()
                column_width = self.column_widths[i]

                pygame.draw.rect(
                    self.screen,
                    self.colors["background"],
                    (xpos, y, column_width + 2 * self.padding, text_rect.height + 2 * self.padding),
                )
                pygame.draw.rect(
                    self.screen,
                    self.colors["border"],
                    (xpos, y, column_width + 2 * self.padding, text_rect.height + 2 * self.padding),
                    1,
                )
                self.screen.blit(
                    text_surface,
                    (xpos + self.padding, y + self.padding)
                )

                xpos += column_width + 2 * self.padding

            y += self.line_height

        self.screen.set_clip(None)

    def sort_list(self, M, left_clicked):
        self.tuple_list = self.quick_sort(self.tuple_list, M)
        if left_clicked and M!=0:
            self.tuple_list.reverse()
        elif left_clicked == False and M == 0:
            self.tuple_list.reverse()

        self.sortby = [M, left_clicked]
    def quick_sort(self, lst, key=0):
        if len(lst) <= 1:
            return lst

        pivot = lst[0]
        left = []
        right = []
        equal = []

        for item in lst:
            if item[key] < pivot[key]:
                left.append(item)
            elif item[key] > pivot[key]:
                right.append(item)
            else:
                equal.append(item)

        sorted_left = self.quick_sort(left, key)
        sorted_right = self.quick_sort(right, key)

        return sorted_left + equal + sorted_right


class TextBox:
    def __init__(self, x, y, width, height, font, char_limit):
        self.rect = pygame.Rect(x, y, width, height)
        self.font = font
        self.char_limit = char_limit
        self.text = ""
        self.is_active = False
        self.text_color = 'white'
        self.box_color = (0, 0, 0)
        self.border_color = (26, 26,26)

    def events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.is_active = self.rect.collidepoint(event.pos)
        elif event.type == pygame.KEYDOWN and self.is_active:
            if event.key == pygame.K_RETURN:
                self.text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif len(self.text) < self.char_limit:
                self.text += event.unicode
            self.text = self.text.upper()

    def render(self, screen):
        pygame.draw.rect(screen, self.box_color, self.rect)
        pygame.draw.rect(screen, self.border_color, self.rect, 2)

        text_surface = self.font.render(self.text, True, self.text_color)
        screen.blit(
            text_surface,
            (self.rect.x + 5, self.rect.y + 5)
        )

from apps.Tetris import game
import pygame
import itertools
from  apps.Tetris import db_stuff
import math



def main():
    pygame.init()

    run = True
    scoreboard = False
    mouse_down = False

    width = 950
    height = 1100
    screen = pygame.display.set_mode((width, height))

    tetris = game.TempObj()

    clock = pygame.time.Clock()

    fps = 60

    colors = ['#000000', '#333333', '#ffffff']
    font_biger = pygame.font.Font(None, 100)
    font_big = pygame.font.Font(None, 75)
    font_small = pygame.font.Font(None, 50)

    font_tetris_big = pygame.font.Font('apps/Tetris/font/tetris.ttf', 60)
    font_tetris_small = pygame.font.Font('apps/Tetris/font/tetris.ttf', 30)
    font_tetris_smaller = pygame.font.Font('apps/Tetris/font/tetris.ttf', 20)
    font_tetris_smallest = pygame.font.Font('apps/Tetris/font/tetris.ttf', 15)

    score_text = font_tetris_small.render('SCORE:', False, colors[2])
    score_text_rect = score_text.get_rect()
    score_text_rect.center = (750, 100)

    score = font_tetris_big.render(str(tetris.score), False, colors[2])
    score_rect = score.get_rect()
    # score_rect.x = 615
    # score_rect.y = 175
    score_rect.center = (750, 175)

    button = font_tetris_smallest.render('SCOREBOARD', False, colors[2])
    button_rect = button.get_rect()
    button_rect.center = (750, 950)

    list = font_tetris_small.render('NEXT:', False, colors[2])
    list_rect = list.get_rect()
    list_rect.center = (750, 337.5)

    lvl_text = font_tetris_small.render('LEVEL:', False, colors[2])
    lvl_text_rect = lvl_text.get_rect()
    lvl_text_rect.center = (720, 775)

    lvl = font_tetris_big.render(str(tetris.level), False, colors[2])
    lvl_rect = lvl.get_rect()
    lvl_rect.center = (825, 775)

    tetris_text = font_tetris_big.render('TETRIS', False, 'white')
    tetris_text_rect = tetris_text.get_rect()
    tetris_text_rect.center = (300, 220)

    start_text = font_tetris_small.render('START', False, 'white')
    start_text_rect = start_text.get_rect()
    start_text_rect.center = (300, 920)

    over_text = font_tetris_small.render('GAME OVER', False, 'white')
    over_text_rect = over_text.get_rect()
    over_text_rect.center = (300, 220)

    restart_text = font_tetris_small.render('RESTART', False, 'white')
    restart_text_rect = restart_text.get_rect()
    restart_text_rect.center = (300, 920)

    lines_cleared_text = font_tetris_smallest.render('LINES CLEARED', False, 'white')
    lines_cleared_text_rect = lines_cleared_text.get_rect()
    lines_cleared_text_rect.center = (180, 75)

    lines_cleared = font_tetris_smallest.render(str(tetris.all_lines_cleared), False, 'white')
    lines_cleared_rect = lines_cleared.get_rect()
    lines_cleared_rect.center = (780, 75)

    Level_selector = game.LevelSelector(screen, 100, 560, font_tetris_smallest)

    select_level = font_tetris_smallest.render('SELECT A LEVEL', False, 'white')
    select_level_rect = select_level.get_rect()
    select_level_rect.center = (300, 530)

    scoreboard_text = font_tetris_big.render('SCOREBOARD', False, 'white')
    scoreboard_text_rect = scoreboard_text.get_rect()
    scoreboard_text_rect.center = (475, 100)

    back_text = font_tetris_small.render('BACK', False, 'white')
    back_text_rect = back_text.get_rect()
    back_text_rect.center = (475, 950)

    Text_box = game.TextBox(150, 750, 300, 50, font_tetris_smaller, 9)

    final_score_text = font_tetris_smaller.render(f'SCORE: ', False, 'white')
    final_score_text_rect = final_score_text.get_rect()
    final_score_text_rect.center = (250, 350)

    final_lvl_text = font_tetris_smaller.render(f'LEVEL: ', False, 'white')
    final_lvl_text_rect = final_lvl_text.get_rect()
    final_lvl_text_rect.center = (250, 425)

    final_lc_text = font_tetris_smallest.render(f'LINES CLEARED: ', False, 'white')
    final_lc_text_rect = final_lc_text.get_rect()
    final_lc_text_rect.center = (200, 500)

    final_lc = font_tetris_smaller.render("", False, 'white')
    final_lc_rect = final_lc.get_rect()
    final_lc_rect.center = (200, 500)

    final_score = font_tetris_smaller.render("", False, 'white')
    final_score_rect = final_score.get_rect()
    final_score_rect.center = (200, 350)

    save_text = font_tetris_smaller.render('SAVE', False, 'green')
    save_text_rect = save_text.get_rect()
    save_text_rect.center = (200, 850)

    cancel_text = font_tetris_smaller.render('CANCEL', False, 'red')
    cancel_text_rect = cancel_text.get_rect()
    cancel_text_rect.center = (400, 850)

    name_text = font_tetris_smaller.render('INSERT NAME:', False, 'white')
    name_text_rect = name_text.get_rect()
    name_text_rect.center = (300, 700)

    face = font_biger.render('=^._.^=', False, 'white')
    face_rect = face.get_rect()
    face_rect.center = (300, 700)

    scores_db = db_stuff.Database()
    db_list = scores_db.FetchAll()

    saved = False

    pygame.mixer.init()

    pygame.mixer_music.load('apps/Tetris/music/Theme.mp3')
    pygame.mixer_music.set_volume(0.3)
    pygame.mixer.music.play(-1)

    Scoreboard = game.Scoreboard(screen, ('NAME', 'SCORE', 'LEVEL', 'LINES CLEARED'), db_list, max_height=650)

    logo = pygame.image.load('apps/Tetris/img/logo.png')
    pygame.display.set_icon(logo)
    pygame.display.set_caption('Tetris')

    def color_cycle():
        period = 500
        t = 0
        while True:
            red = int((math.sin(t * 2 * math.pi / period) + 1) * 127.5)
            green = int((math.sin((t * 2 * math.pi / period) + 2 * math.pi / 3) + 1) * 127.5)
            blue = int((math.sin((t * 2 * math.pi / period) + 4 * math.pi / 3) + 1) * 127.5)
            yield (red, green, blue)
            t += 1

    colors_for_tetris_text = itertools.cycle(color_cycle())

    start_menu = True
    game_over_screen = False

    while run:
        for event in pygame.event.get():
            if scoreboard == True and event.type != pygame.QUIT:
                Scoreboard.events(event)

            if event.type == pygame.QUIT:
                run = False
                pygame.mixer.quit()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_down = True
                    x, y = pygame.mouse.get_pos()
                    # print("Mouse Down")

                    if not scoreboard and 600 < x < 900 and 900 < y < 1000:
                        scoreboard = True

                    if start_menu:
                        Level_selector.events(event)

                        if start_text_rect.collidepoint(x, y):
                            start_menu = False
                            tetris = game.Game(screen, 50, 50, Level_selector.level)

                    if game_over_screen:
                        if saved == False:
                            if save_text_rect.collidepoint(x, y):
                                scores_db.insert_score(Text_box.text, final_score_var, final_lvl_var,
                                                       final_lines_cleared)
                                db_list = scores_db.FetchAll()

                                Scoreboard = game.Scoreboard(screen, ('NAME', 'SCORE', 'LEVEL', 'LINES CLEARED'),
                                                             db_list,
                                                             max_height=650)
                                saved = True
                            elif cancel_text_rect.collidepoint(x, y):
                                saved = True
                        else:
                            if restart_text_rect.collidepoint(x, y):
                                pygame.mixer.music.play(-1)
                                game_over_screen = False
                                Level_selector.reset()
                                start_menu = True
                                Text_box.text = ''
                                saved = False
                    if scoreboard:
                        if back_text_rect.collidepoint(x, y):
                            scoreboard = False
                            # start_menu = True
                            Level_selector.reset()

            elif event.type == pygame.MOUSEBUTTONUP:
                mouse_down = False
                # print("Mouse Up")

            else:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if start_menu and scoreboard == False:
                            start_menu = False
                            tetris = game.Game(screen, 50, 50, Level_selector.level)
                        elif game_over_screen and saved == False:
                            if Text_box.text == '':
                                Text_box.text = 'INANE'
                            scores_db.insert_score(Text_box.text, final_score_var, final_lvl_var, final_lines_cleared)
                            db_list = scores_db.FetchAll()

                            Scoreboard = game.Scoreboard(screen, ('NAME', 'SCORE', 'LEVEL', 'LINES CLEARED'), db_list,
                                                         max_height=650)
                            saved = True
                        elif game_over_screen and saved == True:
                            pygame.mixer.music.play(-1)
                            game_over_screen = False
                            Level_selector.reset()
                            start_menu = True
                            Text_box.text = ''
                            saved = False

                    elif event.key == pygame.K_ESCAPE:
                        if game_over_screen and saved == False and scoreboard == False:
                            saved = True
                        elif scoreboard == True:
                            scoreboard = False

                if start_menu:
                    Level_selector.events(event)
                tetris.events(event)

            if game_over_screen and saved == False:
                Text_box.events(event)

        screen.fill(colors[1])

        score = font_tetris_small.render(str(tetris.score), False, colors[2])
        score_rect = score.get_rect()
        score_rect.center = (750, 175)

        lvl = font_tetris_smaller.render(str(tetris.level), False, colors[2])
        lvl_rect = lvl.get_rect()
        lvl_rect.center = (840, 779)

        lines_cleared = font_tetris_smallest.render(str(tetris.all_lines_cleared), False, 'white')
        lines_cleared_rect = lines_cleared.get_rect()
        lines_cleared_rect.right = 520
        lines_cleared_rect.top = 60

        if scoreboard == False:

            pygame.draw.rect(screen, colors[0], pygame.Rect(50, 50, 500, 1000), border_radius=10)
            pygame.draw.rect(screen, colors[0], pygame.Rect(600, 50, 300, 200), border_radius=10)

            pygame.draw.rect(screen, colors[0], pygame.Rect(600, 400, 300, 260), border_radius=10)
            # pygame.draw.rect(screen, colors[0], pygame.Rect(600, 500, 300, 75))
            # pygame.draw.rect(screen, colors[0], pygame.Rect(600, 600, 300, 75))
            # pygame.draw.rect(screen, colors[0], pygame.Rect(600, 700, 300, 75))
            try:
                a = game.DemoBlock(screen, tetris.next[0], tetris.next[1], 600, 400)
                a.render()
            except:
                pass

            pygame.draw.rect(screen, colors[0], pygame.Rect(600, 900, 300, 100), border_radius=20)

            pygame.draw.rect(screen, colors[0], pygame.Rect(600, 700, 300, 150), border_radius=10)

            screen.blit(score_text, score_text_rect)
            screen.blit(score, score_rect)
            screen.blit(button, button_rect)
            screen.blit(list, list_rect)
            screen.blit(lvl_text, lvl_text_rect)
            screen.blit(lvl, lvl_rect)
            # screen.blit(one_line, one_line_rect)
            # screen.blit(two_line, two_line_rect)
            # screen.blit(three_line, three_line_rect)
            # screen.blit(four_line, four_line_rect)

            if start_menu:
                tetris_text_color = next(colors_for_tetris_text)
                tetris_text = font_tetris_big.render('TETRIS', False, tetris_text_color)

                Level_selector.mainloop()

                screen.blit(tetris_text, tetris_text_rect)
                screen.blit(start_text, start_text_rect)
                screen.blit(select_level, select_level_rect)


            elif game_over_screen:
                over_text_color = next(colors_for_tetris_text)
                over_text = font_tetris_small.render('GAME OVER', False, over_text_color)

                final_score = font_tetris_smaller.render(str(final_score_var), False, 'white')
                final_score_rect = final_score.get_rect()
                final_score_rect.center = (400, 350)

                final_lvl = font_tetris_smaller.render(str(final_lvl_var), False, 'white')
                final_lvl_rect = final_lvl.get_rect()
                final_lvl_rect.center = (400, 425)

                final_lc = font_tetris_smaller.render(str(final_lines_cleared), False, 'white')
                final_lc_rect = final_lc.get_rect()
                final_lc_rect.center = (400, 500)

                screen.blit(over_text, over_text_rect)
                screen.blit(final_score, final_score_rect)
                screen.blit(final_score_text, final_score_text_rect)
                screen.blit(final_lvl_text, final_lvl_text_rect)
                screen.blit(final_lvl, final_lvl_rect)
                screen.blit(final_lc_text, final_lc_text_rect)
                screen.blit(final_lc, final_lc_rect)

                if saved == False:
                    Text_box.render(screen)
                    screen.blit(save_text, save_text_rect)
                    screen.blit(cancel_text, cancel_text_rect)
                    screen.blit(name_text, name_text_rect)

                else:
                    screen.blit(restart_text, restart_text_rect)

                    face_color = next(colors_for_tetris_text)
                    face = font_biger.render('=^._.^=', False, face_color)

                    screen.blit(face, face_rect)

            tetris.mainloop()
            if tetris.run == False:
                final_score_var = tetris.score
                final_lvl_var = tetris.level
                final_lines_cleared = tetris.all_lines_cleared
                del tetris
                tetris = game.TempObj()
                game_over_screen = True
                pygame.mixer_music.stop()

            elif tetris.run == True:
                pygame.draw.rect(screen, (16, 16, 16), (50, 50, 500, 50), border_radius=10)
                pygame.draw.rect(screen, (26, 26, 26), (50, 50, 500, 50), 5, border_radius=10)
                screen.blit(lines_cleared_text, lines_cleared_text_rect)
                screen.blit(lines_cleared, lines_cleared_rect)

        else:
            screen.fill(colors[1])
            Scoreboard.render()

            scoreboard_text_color = next(colors_for_tetris_text)

            scoreboard_text = font_tetris_big.render('SCOREBOARD', False, scoreboard_text_color)

            screen.blit(scoreboard_text, scoreboard_text_rect)
            screen.blit(back_text, back_text_rect)

        clock.tick(fps)

        pygame.display.update()

if __name__ == '__main__':
    main()
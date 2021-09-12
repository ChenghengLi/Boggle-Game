from Classes import *

# ------------------------------
# Funcion principal del juego
# ------------------------------


def main():
    pygame.init()

    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Boggle Game")


    bg = Backgroud("background.png")
    bg.scale(SCREEN_WIDTH, SCREEN_HEIGHT)
    score = MaxPoint()
    table = ChangeTable()
    b = Board()
    word = ShowWord()
    points = ShowPoints()
    showMenu = SubMenu(word, points)
    note = Note()
    ins_1 = Instruction1()
    ins_2 = Instruction2()
    ins_3 = Instruction3()

    def main_game():
        b.generateBoard(table.table)
        b.calcPos()

        timer_font = pygame.font.Font("o.ttf", 38)
        timer_sec = 120
        timer_text = timer_font.render("Time : " + str(timer_sec // 60).zfill(2) + ":" + str(timer_sec % 60).zfill(2),
                                       True, (255, 255, 255))

        timer = pygame.USEREVENT + 1
        pygame.time.set_timer(timer, 1000)


        while True:

            bg.display(screen)
            b.display(screen)
            showMenu.display(screen)
            screen.blit(timer_text, (200, 20))
            ins_2.display(screen)
            ins_1.display(screen)
            ins_3.display(screen)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    b.update(event, screen, word, points)

                if event.type == pygame.QUIT:
                    sys.exit(0)
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        return
                if event.type == timer:  # checks for timer event
                    if timer_sec > 0:
                        timer_sec -= 1
                        timer_text = timer_font.render("Time : " + str(timer_sec//60).zfill(2)+":" + str(timer_sec%60).zfill(2), True, (255, 255, 255))
                    else:
                        pygame.time.set_timer(timer, 0)
                        score.update(table.table, points.points)
                        return

    def start_game():

        st = Start()

        while True:
            bg.display(screen)
            score.display(screen, table.table)
            st.display(screen)
            table.display(screen)
            note.display(screen)
            pygame.display.flip()

            for event in pygame.event.get():

                if event.type == pygame.MOUSEBUTTONDOWN:
                    if st.rect.collidepoint(event.pos):
                        return;
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_4:
                        table.update(4)
                    elif event.key == pygame.K_5:
                        table.update(5)
                    elif event.key == pygame.K_6:
                        table.update(6)
                    elif event.key == pygame.K_RETURN:
                        return

                if event.type == pygame.QUIT:
                    sys.exit(0)


    while True:

        start_game()
        main_game()







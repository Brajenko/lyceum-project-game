import pygame_menu

black = (0, 0, 0, 0)
font = 'pixelfont.ttf'

menu_theme = pygame_menu.Theme(background_color=black,
                               title_background_color=black,
                               widget_font=font,
                               title_font=font,
                               widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(arrow_size=(10, 15),
                                                                                              arrow_right_margin=5,
                                                                                              arrow_vertical_offset=0,
                                                                                              blink_ms=100),
                               widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                               title_offset=(350, 100)
                               )

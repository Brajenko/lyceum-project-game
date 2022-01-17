import pygame_menu
import os

black = (0, 0, 0, 0)
font = 'pixelfont.ttf'

start_im = pygame_menu.baseimage.BaseImage(
    image_path=os.path.join('data', 'menu.jpg'),
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)


finish_im = pygame_menu.baseimage.BaseImage(
    image_path=os.path.join('data', 'finish_menu.jpg'),
    drawing_mode=pygame_menu.baseimage.IMAGE_MODE_FILL
)

start_menu_theme = pygame_menu.Theme(background_color=start_im,
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

finish_menu_theme = pygame_menu.Theme(background_color=finish_im,
                                      title_background_color=black,
                                      widget_font=font,
                                      title_font=font,
                                      widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
                                          arrow_size=(10, 15),
                                          arrow_right_margin=5,
                                          arrow_vertical_offset=0,
                                          blink_ms=100),
                                      widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                                      title_offset=(350, 100)
                                      )

ingame_menu_theme = pygame_menu.Theme(background_color=black,
                                      title_background_color=black,
                                      widget_font=font,
                                      title_font=font,
                                      widget_selection_effect=pygame_menu.widgets.LeftArrowSelection(
                                          arrow_size=(10, 15),
                                          arrow_right_margin=5,
                                          arrow_vertical_offset=0,
                                          blink_ms=100),
                                      widget_alignment=pygame_menu.locals.ALIGN_CENTER,
                                      title_offset=(350, 100)
                                      )

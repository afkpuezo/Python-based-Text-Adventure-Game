"""
This file/module contains the code for displaying the game on a PC using pygame. I'm not sure exactly how much porting
work would/will have to be done, but this seems like a reasonable way to label/divide this code for now.

I really need to work on what I put in these documentations, lol.

started 08/01/20
"""
# imports -----------
from game_view.game_view import GameView
from game_controller.game_controller import GameController
from game_model.game_model import TextLocationKey  # TODO this class should be moved probably
from typing import Dict  # lets try this again
from typing import List

# pygame imports (i suspect will need a lot of tweaking over time)
import pygame
import pygame.font

# actual code ---------------------
class WindowStats:
    """
    enum* for stuff like resolution, etc
    """
    WINDOW_WIDTH = 1000
    WINDOW_HEIGHT = 750
    WINDOW_NAME = "spoopy hows gaem"

    LEFT_MARGIN = 20
    TOP_MARGIN = 20
    RIGHT_MARGIN = 20
    BOTTOM_MARGIN = 20

    TOTAL_TEXT_AREA_HEIGHT = WINDOW_HEIGHT - (TOP_MARGIN - BOTTOM_MARGIN)
    TEXT_WIDTH = (WINDOW_WIDTH - LEFT_MARGIN) - RIGHT_MARGIN

    FONT_SIZE = 32
    SPACE_BETWEEN_LINES = 5
    TEXT_LINE_LENGTH = WINDOW_WIDTH - (LEFT_MARGIN + RIGHT_MARGIN)

    # main and event are top-justified
    MAIN_TEXT_ANCHOR = (LEFT_MARGIN, TOP_MARGIN)
    MAIN_TEXT_HEIGHT = TOTAL_TEXT_AREA_HEIGHT / 2
    # MAIN_TEXT_HEIGHT = (FONT_SIZE + SPACE_BETWEEN_LINES) * 6
    BETWEEN_MAIN_AND_EVENT = WINDOW_HEIGHT / 30

    EVENT_TEXT_ANCHOR = (LEFT_MARGIN, (MAIN_TEXT_ANCHOR[1] + MAIN_TEXT_HEIGHT + BETWEEN_MAIN_AND_EVENT))  # a mess
    EVENT_TEXT_HEIGHT = TOTAL_TEXT_AREA_HEIGHT / 10
    # EVENT_TEXT_HEIGHT = (FONT_SIZE + SPACE_BETWEEN_LINES) * 1
    BETWEEN_EVENT_AND_PROMPT = WINDOW_HEIGHT / 10

    # prompt and input are bottom-justified
    INPUT_TEXT_HEIGHT = TOTAL_TEXT_AREA_HEIGHT / 10
    # INPUT_TEXT_HEIGHT = (FONT_SIZE + SPACE_BETWEEN_LINES) * 1
    INPUT_TEXT_ANCHOR = (LEFT_MARGIN, (WINDOW_HEIGHT - BOTTOM_MARGIN - INPUT_TEXT_HEIGHT))
    BETWEEN_PROMPT_AND_INPUT = WINDOW_HEIGHT / 30

    PROMPT_TEXT_HEIGHT = TOTAL_TEXT_AREA_HEIGHT / 10
    # PROMPT_TEXT_HEIGHT = (FONT_SIZE + SPACE_BETWEEN_LINES) * 1
    PROMPT_TEXT_ANCHOR = (LEFT_MARGIN, (INPUT_TEXT_ANCHOR[1] - BETWEEN_PROMPT_AND_INPUT - PROMPT_TEXT_HEIGHT))

    # colors and stuff
    BACKGROUND_COLOR = (0, 0, 0)  # black
    TEXT_COLOR = (255, 255, 255)  # white

    # colors for the test text boxes - these aren't 'stats', strictly speaking
    TEST_MAIN_BG_COLOR = (128, 128, 128)
    TEST_EVENT_BG_COLOR = (255, 0, 0)
    TEST_PROMPT_BG_COLOR = (0, 255, 0)
    TEST_INPUT_BG_COLOR = (0, 0, 255)
# end WindowStats class

class PCPygameGameView(GameView):
    """
    Handles displaying the text output of the game in a window using pygame. Pings the controller when it needs the
    model to process player input. Implements/extends the GameView interface / abstract class. Also is a mouthful to say
    """

    # stuff from GameView ------------------------
    def game_launched(self, output_text: Dict[str, str]):
        """
        Initializes pygame and opens the window.

        :return: True if initialization successful, false otherwise.
        """
        pygame.init()
        pygame.display.set_caption(WindowStats.WINDOW_NAME)
        self.screen = pygame.display.set_mode((WindowStats.WINDOW_WIDTH, WindowStats.WINDOW_HEIGHT))
        self.font = pygame.font.SysFont(None, WindowStats.FONT_SIZE)

        self.show_text_boxes()
        self.draw_all_output_text(output_text)

        frames = 0

            
        while(frames < 7000):
            frames += 1
            pygame.display.flip()
    # end game_launched method

    def game_closing(self):
        """
        What to do when the user quits. TODO IDK if this is even a thing

        :return:
        """
        pass

    # stuff specifically for PCPygameGameView -------------

    def __init__(self, controller: GameController):
        """
        The constructor. Will not actually initialize pygame stuff or open the window frame.

        :param controller: The GameController for this View.
        """
        self.controller: GameController = controller
        self.screen: pygame.Surface = None
        self.font: pygame.Font = None

        self.text_rects: Dict[str, pygame.Rect] = dict()
        self.text_rects[TextLocationKey.MAIN] = pygame.Rect(WindowStats.MAIN_TEXT_ANCHOR,
                                                            (WindowStats.TEXT_WIDTH, WindowStats.MAIN_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.EVENT] = pygame.Rect(WindowStats.EVENT_TEXT_ANCHOR,
                                                             (WindowStats.TEXT_WIDTH, WindowStats.EVENT_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.PROMPT] = pygame.Rect(WindowStats.PROMPT_TEXT_ANCHOR,
                                                              (WindowStats.TEXT_WIDTH, WindowStats.PROMPT_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.INPUT] = pygame.Rect(WindowStats.INPUT_TEXT_ANCHOR,
                                                              (WindowStats.TEXT_WIDTH, WindowStats.INPUT_TEXT_HEIGHT))
    # end constructor

    def show_text_boxes(self):
        """
        Shows colored boxes on the screen, demonstrating where the text areas are. Used for testing/debugging.

        :return:
        """
        text_surfaces: Dict[str, pygame.Surface] = dict()

        text_surfaces[TextLocationKey.MAIN] = pygame.Surface((WindowStats.TEXT_WIDTH,
                                                              WindowStats.MAIN_TEXT_HEIGHT))
        text_surfaces[TextLocationKey.EVENT] = pygame.Surface((WindowStats.TEXT_WIDTH,
                                                               WindowStats.EVENT_TEXT_HEIGHT))
        text_surfaces[TextLocationKey.PROMPT] = pygame.Surface((WindowStats.TEXT_WIDTH,
                                                                WindowStats.PROMPT_TEXT_HEIGHT))
        text_surfaces[TextLocationKey.INPUT] = pygame.Surface((WindowStats.TEXT_WIDTH,
                                                               WindowStats.INPUT_TEXT_HEIGHT))

        text_surfaces[TextLocationKey.MAIN].fill(WindowStats.TEST_MAIN_BG_COLOR)
        self.screen.blit(text_surfaces[TextLocationKey.MAIN], self.text_rects[TextLocationKey.MAIN])
        text_surfaces[TextLocationKey.EVENT].fill(WindowStats.TEST_EVENT_BG_COLOR)
        self.screen.blit(text_surfaces[TextLocationKey.EVENT], self.text_rects[TextLocationKey.EVENT])
        text_surfaces[TextLocationKey.PROMPT].fill(WindowStats.TEST_PROMPT_BG_COLOR)
        self.screen.blit(text_surfaces[TextLocationKey.PROMPT], self.text_rects[TextLocationKey.PROMPT])
        text_surfaces[TextLocationKey.INPUT].fill(WindowStats.TEST_INPUT_BG_COLOR)
        self.screen.blit(text_surfaces[TextLocationKey.INPUT], self.text_rects[TextLocationKey.INPUT])

        # now fill in the insides of those rects with black so the outlines look cool
        TEXT_BOX_OUTLINE_MARGIN = 1

        outline_rects: list[pygame.Rect] = list()
        for key in self.text_rects:
            r = self.text_rects[key]
            out_r = pygame.Rect(r.left + TEXT_BOX_OUTLINE_MARGIN,
                                r.top + TEXT_BOX_OUTLINE_MARGIN,
                                WindowStats.TEXT_LINE_LENGTH - (2 * TEXT_BOX_OUTLINE_MARGIN),
                                r.height - (2 * TEXT_BOX_OUTLINE_MARGIN))
            self.screen.fill(WindowStats.BACKGROUND_COLOR, out_r)
    # end show_text_boxes method

    def draw_all_output_text(self, output_text: Dict[str, str]):
        """
        Writes the given output text onto the screen. The key for each entry in the
        output_text dict should correspond to which text field (Main, event, etc) they will go to.

        Will not refresh the screen - do that before you call it.

        TODO only draw what's changed? I don't really think framerate is going to be a problem

        :param output_text: a Dict of strings - one string per text area (main, event, etc)
        :return:
        """
        # self.screen.fill(WindowStats.BACKGROUND_COLOR)
        self.draw_one_text_area(output_text[TextLocationKey.MAIN],
                                WindowStats.MAIN_TEXT_ANCHOR,
                                WindowStats.MAIN_TEXT_HEIGHT)
        self.draw_one_text_area(output_text[TextLocationKey.EVENT],
                                WindowStats.EVENT_TEXT_ANCHOR,
                                WindowStats.EVENT_TEXT_HEIGHT)
        self.draw_one_text_area(output_text[TextLocationKey.PROMPT],
                                WindowStats.PROMPT_TEXT_ANCHOR,
                                WindowStats.PROMPT_TEXT_HEIGHT)

    # end draw_all_output_text

    def draw_one_text_area(self, text: str, anchor: tuple, max_height: int):
        """
        Draws (writes?) the given text, using the given anchor as the top left. Text (should) will be bounded by the
        height of the text area, and the generic text area width.

        :param text: The text to draw
        :param anchor: The top-left corner of the text area (EG where to start)
        :param max_height: The height of the text area (EG the limit of our space)
        :return:
        """
        # are we going to need to wraparound (more than one line?)
        if self.font.size(text)[0] < WindowStats.TEXT_LINE_LENGTH:
            text_image = self.font.render(text, True, WindowStats.TEXT_COLOR)
            self.screen.blit(text_image, anchor)
        else:
            # break it into lines that are short enough
            # total_height = 0  # what is the height of everything we've written?
            words: List[str] = text.split(" ")
            current_line: str = str()
            current_line_length: int = 0
            lines: List[str] = list()  # TODO should these 2 lists (and 1 int) be one list with lines + heights paired?
            line_heights: List[int] = [0]
            num_lines: int = 0
            out_of_space = False

            for word in words:
                # would adding this word to the current line be too long?
                word_length = self.font.size(word + " ")[0]  # include the space after each word
                current_line_length += word_length
                print("DEBUG: WORD:", word, "WORD LENGTH:", word_length, "LINE LENGTH", current_line_length)
                if current_line_length < WindowStats.TEXT_LINE_LENGTH:  # if we're good on this line
                    current_line += word + " "
                else:  # time for a new line
                    print("DEBUG: starting a new line...the old line is <", current_line, ">")
                    lines.append(current_line)
                    num_lines += 1
                    next_line_height = line_heights[-1] + self.font.get_linesize() + WindowStats.SPACE_BETWEEN_LINES
                    if next_line_height < max_height:  # we're good to keep writing lines, so start a new one
                        line_heights.append(next_line_height)
                        current_line = word + " "
                        current_line_length = word_length
                    else:  # we're done writing lines
                        out_of_space = True
                        break
            # end line-generating for loop

            # OMG i didn't think to draw the last line that's been stored after the loop ends
            if not out_of_space:
                lines.append(current_line)
                line_heights.append(next_line_height)
                num_lines += 1

            # now actually display it all
            for L in range(0, num_lines):
                text_image = self.font.render(lines[L], True, WindowStats.TEXT_COLOR)
                self.screen.blit(text_image, (anchor[0], anchor[1] + line_heights[L]))
            # end blitting lines for loop
    # end draw_one_text_area
# end PCPygameGameView class

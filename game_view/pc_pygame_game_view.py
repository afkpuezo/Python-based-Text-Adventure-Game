"""
This file/module contains the code for displaying the game on a PC using pygame. I'm not sure exactly how much porting
work would/will have to be done, but this seems like a reasonable way to label/divide this code for now.

I really need to work on what I put in these documentations, lol.

started 08/01/20

I might as well put the link to the tutorial I used in here:
https://pygame.readthedocs.io/en/latest/4_text/text.html
"""
# imports -----------
from game_view.game_view import GameView
# from game_controller.game_controller import GameController
from utilities.game_enums import TextLocationKey
from typing import Dict  # lets try this again
from typing import List

# pygame imports (i suspect will need a lot of tweaking over time)
import pygame
from pygame.locals import * # not sure exactly what's in here lol
import pygame.font
import time

# actual code ---------------------
class WindowStats:
    """
    Enum* for stuff like resolution, etc. Maybe some of this should be split into other classes, or all put into
    PCPyGameView? Ugh this is so haaaaaaaaaaaaaaard
    """
    WINDOW_WIDTH = 960
    WINDOW_HEIGHT = 840
    WINDOW_NAME = "spoopy hows gaem"

    LEFT_MARGIN = int(WINDOW_WIDTH / 100) * 2
    TOP_MARGIN = int(WINDOW_HEIGHT / 100) * 2
    RIGHT_MARGIN = int(WINDOW_WIDTH / 100) * 2
    BOTTOM_MARGIN = int(WINDOW_HEIGHT / 100) * 2

    TOTAL_TEXT_AREA_HEIGHT = WINDOW_HEIGHT - (TOP_MARGIN - BOTTOM_MARGIN)
    TEXT_WIDTH = (WINDOW_WIDTH - LEFT_MARGIN) - RIGHT_MARGIN
    FONT_SIZE: int = int((TOTAL_TEXT_AREA_HEIGHT / 100) * 4)

    SPACE_BETWEEN_LINES = 0
    TEXT_LINE_LENGTH = WINDOW_WIDTH - (LEFT_MARGIN + RIGHT_MARGIN)

    # main and event are top-justified
    MAIN_TEXT_ANCHOR = (LEFT_MARGIN, TOP_MARGIN)
    MAIN_TEXT_HEIGHT = int((FONT_SIZE + SPACE_BETWEEN_LINES) * 10.9)
    BETWEEN_MAIN_AND_EVENT = int(FONT_SIZE * .75)

    EVENT_TEXT_ANCHOR = (LEFT_MARGIN, (MAIN_TEXT_ANCHOR[1] + MAIN_TEXT_HEIGHT + BETWEEN_MAIN_AND_EVENT))  # a mess
    EVENT_TEXT_HEIGHT = int((FONT_SIZE + SPACE_BETWEEN_LINES) * 2.25)

    # prompt and input are bottom-justified
    # INPUT_TEXT_HEIGHT: int = TOTAL_TEXT_AREA_HEIGHT / 10
    INPUT_TEXT_HEIGHT = int((FONT_SIZE + SPACE_BETWEEN_LINES) * 1)
    INPUT_TEXT_ANCHOR = (LEFT_MARGIN, (WINDOW_HEIGHT - BOTTOM_MARGIN - INPUT_TEXT_HEIGHT))
    BETWEEN_PROMPT_AND_INPUT = int(FONT_SIZE * .25)

    PROMPT_TEXT_HEIGHT = int((FONT_SIZE + SPACE_BETWEEN_LINES) * 1)
    PROMPT_TEXT_ANCHOR = (LEFT_MARGIN, (INPUT_TEXT_ANCHOR[1] - BETWEEN_PROMPT_AND_INPUT - PROMPT_TEXT_HEIGHT))

    BETWEEN_CURSOR_AND_INPUT = 0  # these three control how big the cursor is
    CURSOR_ANCHOR_HEIGHT_DISPLACEMENT = int(FONT_SIZE / -5)
    CURSOR_WIDTH = int(FONT_SIZE / 15)
    CURSOR_HEIGHT = int(FONT_SIZE * 1)
    CURSOR_TIME_UNIT = 1  # these two control how fast the cursor blinks
    CURSOR_BLINK_RATE = 0.5

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

    # class attributes ----------------
    # TODO should these be 'enums'?
    # this one is unicodes cuz its faster to type lul
    ALLOWED_KEY_UNICODES: List[str] = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm',
                                       'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z',
                                       ' ', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
    # these are actually event.keys
    DELETE_KEYS: List[int] = [K_BACKSPACE, K_DELETE]
    ENTER_KEYS: List[int] = [K_KP_ENTER, K_RETURN]

    # stuff from GameView ------------------------
    def game_launched(self, output_texts: Dict[str, str]):
        """
        Initializes pygame and opens the window.

        :param output_texts: The initial text to be displayed
        :return: True if initialization successful, false otherwise.
        """
        pygame.init()
        pygame.display.set_caption(WindowStats.WINDOW_NAME)
        self.screen = pygame.display.set_mode((WindowStats.WINDOW_WIDTH, WindowStats.WINDOW_HEIGHT))
        self.font = pygame.font.SysFont(None, WindowStats.FONT_SIZE)

        # self.show_text_boxes()
        self.draw_all_output_text(output_texts)

        self.game_view_loop()
    # end game_launched method

    def game_closing(self):
        """
        What to do when the user quits. Called by the controller when the model indicates the player has decided to
        quit. Currently it just sets the self.running to False, so the loop will stop and the window will close.

        :return:
        """
        self.running = False
    # end player_quit method

    def set_controller(self, controller):
        """
        Called by the controller to connect itself to the view.
        (I don't know if this is necessary but it seems safer?)

        :param controller: The GameController
        :return:
        """
        self.controller = controller
    # end set_controller method

    # stuff specifically for PCPygameGameView -------------

    def __init__(self):
        """
        The constructor. Will not actually initialize pygame stuff or open the window frame.

        """
        self.controller = None # will be set directly by the controller itself
        self.screen: pygame.Surface = None
        self.font: pygame.Font = None
        self.running = False  # does this need to be an instance attribute? or should it just be in the _loop method?
        self.input_text: str = str()  # same deal as with the above i guess?

        self.text_rects: Dict[str, pygame.Rect] = dict()
        self.text_rects[TextLocationKey.MAIN] = pygame.Rect(WindowStats.MAIN_TEXT_ANCHOR,
                                                            (WindowStats.TEXT_WIDTH, WindowStats.MAIN_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.EVENT] = pygame.Rect(WindowStats.EVENT_TEXT_ANCHOR,
                                                             (WindowStats.TEXT_WIDTH, WindowStats.EVENT_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.PROMPT] = pygame.Rect(WindowStats.PROMPT_TEXT_ANCHOR,
                                                              (WindowStats.TEXT_WIDTH, WindowStats.PROMPT_TEXT_HEIGHT))
        self.text_rects[TextLocationKey.INPUT] = pygame.Rect(WindowStats.INPUT_TEXT_ANCHOR,
                                                              (WindowStats.TEXT_WIDTH, WindowStats.INPUT_TEXT_HEIGHT))

        self.cursor_rect: pygame.Rect = pygame.Rect(WindowStats.INPUT_TEXT_ANCHOR[0],
                                                    WindowStats.INPUT_TEXT_ANCHOR[1]
                                                    + WindowStats.CURSOR_ANCHOR_HEIGHT_DISPLACEMENT,
                                                    WindowStats.CURSOR_WIDTH,
                                                    WindowStats.CURSOR_HEIGHT)
    # end constructor

    def show_text_boxes(self):
        """
        Shows colored boxes on the screen, demonstrating where the text areas are. Used for testing/debugging. So the
        tutorial I looked at had a way to draw the bounding rectangle *with* the text, but it didn't seem worthwhile to
        change this so I left it this way.

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

    def draw_one_text_area(self, text: str, anchor: tuple, max_height: int, clear_before = False):
        """
        Draws (writes?) the given text, using the given anchor as the top left. Text (should) will be bounded by the
        height of the text area, and the generic text area width.

        :param text: The text to draw
        :param anchor: The top-left corner of the text area (EG where to start)
        :param max_height: The height of the text area (EG the limit of our space)
        :param clear_before: Will clear the area before writing text (aka use screen.fill)
        :return:
        """

        if clear_before:
            self.screen.fill(WindowStats.BACKGROUND_COLOR, self.text_rects[TextLocationKey.INPUT])

        # break it into lines that are short enough
        # total_height = 0  # what is the height of everything we've written?
        words: List[str] = text.split(" ")
        current_line: str = str()
        current_line_length: int = 0
        lines: List[str] = list()  # TODO should these 2 lists (and 1 int) be one list with lines + heights paired?
        line_heights: List[int] = [0]
        num_lines: int = 0
        out_of_space = False
        next_line_height = 0

        for word in words:
            # would adding this word to the current line be too long?
            word_length = self.font.size(word + " ")[0]  # include the space after each word
            current_line_length += word_length
            # print("DEBUG: word is", word)
            # if word == "\n":
            #     print("DEBUG: newline detected")
            if (current_line_length < WindowStats.TEXT_LINE_LENGTH) and (word != "\n"):  # we're good on this line
                current_line += word + " "
            else:  # time for a new line
                lines.append(current_line)
                num_lines += 1
                next_line_height = line_heights[-1] + self.font.get_linesize() + WindowStats.SPACE_BETWEEN_LINES
                # determine if we have room for at least one more line
                # i'm not sure why I have to count the font linesize again but it makes things fit nicely
                if next_line_height + self.font.get_linesize() < max_height:
                    line_heights.append(next_line_height)
                    if word == '\n':  # don't actually write a newline-character or an extraneous space
                        current_line = str()
                        current_line_length = 0
                    else: # start the new line with the current word
                        current_line = word + " "
                        current_line_length = self.font.size(current_line)
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

    def game_view_loop(self):
        """
        Executes the core loop of the GameView (lmao that wording). Displays main, event, and prompt text based on the
        GameModel (thru the GameController), and handles updating/displaying the player's input text.

        :return:
        """
        self.running = True
        updated_input: bool = False
        output_text: str = str()
        pygame.display.update()
        updated_rects: List[pygame.Rect] = list()

        while self.running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False
                if event.type == KEYDOWN:
                    if event.key in PCPygameGameView.DELETE_KEYS:
                        self.input_text = self.input_text[:-1]  # slice off the last character (safe when empty)
                        updated_input = True
                    elif event.key in PCPygameGameView.ENTER_KEYS:
                        output_text = self.send_text_to_controller()  # TODO update this later
                        self.screen.fill(WindowStats.BACKGROUND_COLOR)
                        self.draw_all_output_text(output_text)
                        updated_rects.append(self.text_rects[TextLocationKey.MAIN])
                        updated_rects.append(self.text_rects[TextLocationKey.EVENT])
                        updated_rects.append(self.text_rects[TextLocationKey.PROMPT])
                        self.input_text = ""
                        updated_input = True
                    else:
                        input_ch = event.unicode.lower()  # only let them type lower case
                        if input_ch in PCPygameGameView.ALLOWED_KEY_UNICODES:
                            # make sure the input text isn't too long
                            if self.font.size(self.input_text + input_ch)[0] < WindowStats.TEXT_LINE_LENGTH:
                                self.input_text += input_ch
                                updated_input = True
            # end event handling for loop
            if updated_input:
                self.screen.fill(WindowStats.BACKGROUND_COLOR, self.cursor_rect)  # TODO a placeholder solution?
                updated_rects.append(self.cursor_rect.copy())  # has to copy cuz it might be changed later
                self.draw_one_text_area(self.input_text,
                                        WindowStats.INPUT_TEXT_ANCHOR,
                                        WindowStats.INPUT_TEXT_HEIGHT,
                                        True)
                updated_rects.append(self.text_rects[TextLocationKey.INPUT])
            # end if updated_input
            # now handle the cursor
            updated_rects.append(self.update_cursor(updated_input))

            updated_input = False # reset this for next frame

            # now actually _update_ the screen lmao
            pygame.display.update(updated_rects)
        # end while loop
    # end game_view_loop method

    def update_cursor(self, updated_input: bool) -> pygame.Rect:
        """
        Ensures that the blinking cursor is always at the end of the input text and actually blinks.
        TODO so I'm not tracking whether the cursor is currently on, it would save some calculations but it's
        TODO to write so I'm just not going to bother

        :param updated_input: Whether the input text was updated in this frame (and therefore the cursor should move)
        :return:
        """
        if updated_input:
            # we don't need to clear the old cursor because writing the text did it already
            self.cursor_rect.x = WindowStats.INPUT_TEXT_ANCHOR[0] \
                                 + self.font.size(self.input_text)[0] \
                                 + WindowStats.BETWEEN_CURSOR_AND_INPUT
            self.cursor_rect.y = WindowStats.INPUT_TEXT_ANCHOR[1] + WindowStats.CURSOR_ANCHOR_HEIGHT_DISPLACEMENT

        if time.time() % WindowStats.CURSOR_TIME_UNIT > WindowStats.CURSOR_BLINK_RATE:
            self.screen.fill(WindowStats.TEXT_COLOR, self.cursor_rect)
            return self.cursor_rect  # let the loop know to update this
        else:
            self.screen.fill(WindowStats.BACKGROUND_COLOR, self.cursor_rect)
            return self.cursor_rect  # let the loop know to update this

    # end update_cursor method

    def send_text_to_controller(self) -> Dict[str, str]:
        """
        Sends the current self.input_text to the controller, who will send it to the model. Will return the output texts
        back to the loop method.

        :return: The output texts back to the loop method.
        """
        return self.controller.send_input_text_to_model(self.input_text)
    # end send_text_to_controller method
# end PCPygameGameView class
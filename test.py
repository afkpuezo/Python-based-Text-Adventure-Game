from game_view.pc_pygame_game_view import PCPygameGameView
from game_model.game_model import TextLocationKey

output_text = dict()
output_text[TextLocationKey.MAIN] = "This is a rather long text string as a test to make sure my code works. Let's try to make it three lines maybe? Here we go let's check. " * 10
output_text[TextLocationKey.EVENT] = "Here is the event text. " * 10
output_text[TextLocationKey.PROMPT] = "Here is the prompt text. " * 10

view = PCPygameGameView(None)
view.game_launched(output_text)






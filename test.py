from game_controller.pc_game_controller import PCGameController
from game_model.pc_game_model import PCGameModel
from game_view.pc_pygame_game_view import PCPygameGameView

model = PCGameModel()
view = PCPygameGameView()
controller = PCGameController(model, view)
controller.game_launched()

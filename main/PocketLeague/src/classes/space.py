import pymunk

def player_ball_collision_handler(arbiter, space, data):
    print(f"{data['player'].get_name()} touched the ball")
    return True

class Space:

    space: pymunk.Space = pymunk.Space()

    id = 1

    def add_mapping(id, player):
        handler = Space.space.add_collision_handler(id, 0) # player_collision_type, ball_collision_type
        handler.begin = player_ball_collision_handler
        handler.data["player"] = player

    def get_and_incr_id():
        n = Space.id
        Space.id += 1
        return n

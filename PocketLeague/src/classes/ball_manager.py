from .ball import Ball


class BallManager:

    ball: Ball = None

    @staticmethod
    def create_ball(ball_bounciness):
        BallManager.ball = Ball(ball_bounciness)

    @staticmethod
    def destroy_ball():
        BallManager.ball = None

    @staticmethod
    def get_ball():
        return BallManager.ball

    @staticmethod
    def reset_ball():
        BallManager.ball.reset()

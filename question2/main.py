from game import Game
import logging

logging.basicConfig(level=logging.ERROR)

def main():
    try:
        game = Game()
        game.run()
    except Exception as e:
        logging.error(f"Error in main: {e}")

if __name__ == "__main__":
    main()

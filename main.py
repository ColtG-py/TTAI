from world_nav.player_controller import PlayerController


def main():
    player_loco = PlayerController()
    while True:
        player_loco.press_up()

if __name__ == "__main__":
    main()
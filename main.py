import pygame as pg
from phasemanager import PhaseManager

def main():
    pg.init()
    screen = pg.display.set_mode((1920, 1080))
    pg.display.set_caption("Expose-SVT")

    phase_manager = PhaseManager(
        phases_file="phases.json",
        dialogues_file="dialogues.json",
        minigame_configs="minigameconfig.json",
        screen=screen
    )

    running = True
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

        screen.fill("black")
        if not phase_manager.start_phase():
            running = False  # Exit loop when all phases are completed

        pg.display.flip()
        pg.time.wait(1000)  # Simulate phase duration

    pg.quit()

if __name__ == "__main__":
    main()


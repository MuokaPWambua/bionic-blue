
### third-party imports

from pygame import quit as quit_pygame

from pygame.locals import (

    QUIT,
    K_a, K_d,

    KEYDOWN,
    K_ESCAPE,
    K_j, K_k
)

from pygame.event import get as get_events

from pygame.key import get_pressed as get_pressed_state

from pygame.time import get_ticks as get_msecs


### local imports

from ....config import (
    PROJECTILES,
    MAX_X_SPEED,
    SHOOTING_STANCE_MSECS,
    DAMAGE_REBOUND_MSECS,
)

from .projectiles.default import DefaultProjectile



class WalkRight:

    def walk_right_control(self):

        ###

        for event in get_events():

            if event.type == QUIT:
                quit_pygame()
                quit()

            elif event.type == KEYDOWN:

                if event.key == K_ESCAPE:
                    quit_pygame()
                    quit()

                elif event.key == K_j:
                    self.walk_right_shoot()

                elif event.key == K_k:
                    self.jump()

        ###

        pressed_state = get_pressed_state()

        if pressed_state[K_a]:

            self.x_accel += -1

            if self.aniplayer.anim_name == 'shooting_walk_right':
                self.set_state('decelerate_right')
                self.aniplayer.blend('+shooting')

            else:
                self.set_state('decelerate_right')

        elif pressed_state[K_d]:
            self.x_accel = min(self.x_accel + 1, 2)

        else:
            self.x_accel = max(self.x_accel - 1, 0)

    def walk_right_update(self):

        x = self.rect.x

        if self.x_speed > 0:
            self.x_speed += -1

        self.x_speed += self.x_accel
        self.x_speed = min(max(self.x_speed, 0), MAX_X_SPEED)

        self.rect.x += self.x_speed

        if not self.x_speed: self.set_state('idle_right')

        if get_msecs() - self.last_shot >= SHOOTING_STANCE_MSECS:
            self.aniplayer.blend('-shooting')

        if self.rect.x != x:
            self.avoid_blocks_horizontally()

        self.react_to_gravity()

        if get_msecs() - self.last_damage > DAMAGE_REBOUND_MSECS:
            self.aniplayer.restore_constant_drawing()

    def walk_right_shoot(self):

        pos_value = self.rect.move(0, -2).midright
        projectile = DefaultProjectile(x_orientation=1, pos_name='center', pos_value=pos_value)
        PROJECTILES.add(projectile)
        self.aniplayer.ensure_animation('shooting_walk_right')
        self.last_shot = get_msecs()
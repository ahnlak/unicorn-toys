# rain.py - from the unicorn-toys collection
#
# This is an implementation of the terminal-era 'rain' program - it simulates
# rain falling on your Unicorn!
#
# Copyright (C) 2022 Pete Favelle <ahnlak@gmail.com>
# Released under the MIT License; see LICENSE for details

import machine, random, time
from math import trunc
from galactic import GalacticUnicorn
from picographics import PicoGraphics, DISPLAY_GALACTIC_UNICORN

# Create the Unicorn object and the graphics surface
galactic = GalacticUnicorn()
graphics = PicoGraphics(DISPLAY_GALACTIC_UNICORN)

# We'll maintain a list of raindrops
raindrops = []
palette = [
  graphics.create_pen(255, 255, 255),
  graphics.create_pen( 50,  50, 150),
  graphics.create_pen( 40,  40, 100),
  graphics.create_pen( 30,  30,  80),
  graphics.create_pen( 20,  20,  50),
  graphics.create_pen( 10,  10,  20),
  graphics.create_pen(  5,   5,  10),
]


# Small class to wrangle said raindrops
class Raindrop:
  def __init__(self, x, y):
    self.x = x
    self.y = y
    self.lifespan = 1

  def draw(self):
    # Set the right colour, based on our age
    graphics.set_pen(palette[self.lifespan])

    graphics.circle(self.x, self.y, self.lifespan)
    if self.lifespan > 1:
      graphics.set_pen(graphics.create_pen(0, 0, 0))
      graphics.circle(self.x, self.y, self.lifespan-1)
    if self.lifespan > 4:
      graphics.set_pen(palette[self.lifespan])
      graphics.circle(self.x, self.y, 1)

  def update(self):
    self.lifespan += 1

  def is_alive(self):
    return self.lifespan < 7


# So, the main loop - we check to see if we need new raindrops, then
# render through them all, and ... breathe
while True:

  # Clear the screen so we know what we're doing
  graphics.set_pen(graphics.create_pen(0, 0, 0))
  graphics.clear()

  # Clear out any expired raindrops
  raindrops = [drop for drop in raindrops if drop.is_alive()]

  # Do we have enough raindrops?
  if len(raindrops) < random.randint(4, 10):
    newdrop=Raindrop(1,2)
    raindrops.append(Raindrop(random.randint(0,GalacticUnicorn.WIDTH),random.randint(0,GalacticUnicorn.HEIGHT)))

  # So, ask each of those raindrops to render themselves, and update
  for drop in raindrops:
    drop.draw()
    drop.update()

  # And update the screen
  galactic.update(graphics)

  # Nice. So, breathe...
  time.sleep(0.15)

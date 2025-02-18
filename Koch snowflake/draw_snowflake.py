# %%
from PIL import Image, ImageDraw
from math import cos, sin, radians

# %%


def koch_snowflake(draw, order, size, start, angle=0):
    if order == 0:
        end = (
            start[0] + size * cos(radians(angle)),
            start[1] + size * sin(radians(angle)),
        )
        draw.line([start, end], fill="black", width=1)
        return end
    else:
        size /= 3
        start = koch_snowflake(draw, order - 1, size, start, angle)
        start = koch_snowflake(draw, order - 1, size, start, angle + 60)
        start = koch_snowflake(draw, order - 1, size, start, angle - 60)
        start = koch_snowflake(draw, order - 1, size, start, angle)
        return start


def draw_snowflake(order):
    size = 300
    image_size = (size * 2, size * 2)
    image = Image.new("RGB", image_size, "white")
    draw = ImageDraw.Draw(image)

    start = (image_size[0] / 2 - size/2, image_size[1]/2+size/4)
    for angle in [0, -120, 120]:
        start = koch_snowflake(draw, order, size, start, angle)
        break

    image
    return image


# Set the order of the snowflake (0 for no detail, higher for more detail)
image = draw_snowflake(1)
image

# %%
image = draw_snowflake(10)
display(image)

# %%

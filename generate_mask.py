from PIL import Image, ImageDraw

# create a new image with a white background
img = Image.new('RGB', (600, 600), color='white')

# create a mask using ImageDraw
mask = Image.new('1', (600, 600), 0)
draw = ImageDraw.Draw(mask)
draw.rectangle((200, 200, 400, 400), fill=1)

# apply the mask to the image
img.putalpha(mask)

# save the resulting image as a PNG file
img.save('square_mask.png')

# This program generates ready-to-print labels from a list of labels entered by the user.
# The final result is a PNG image with all the labels stitched together, located in the "output" folder.

# This is not particularly optimized nor clean, but I made it in a hurry and it works.



from PIL import Image, ImageDraw, ImageFont

# The program uses the os library to delete the content of the "labels" and "labels lines" folders
import os

# The program uses the math library to round up the division of the label size by 2048
import math





# Directories
labelDirectory = "labels"
labelLinesDirectory = "labelLines"
outputDirectory = "output"

# Create the directories if they don't exist
if not os.path.exists(labelDirectory):
    os.makedirs(labelDirectory)

if not os.path.exists(labelLinesDirectory):
    os.makedirs(labelLinesDirectory)

if not os.path.exists(outputDirectory):
    os.makedirs(outputDirectory)

# Delete the content of the "labels" folder
for file in os.listdir(labelDirectory):
    os.remove(os.path.join(labelDirectory, file))

# Delete the content of the "labels lines" folder
for file in os.listdir(labelLinesDirectory):
    os.remove(os.path.join(labelLinesDirectory, file))

# Font size
fontSize = 100

# Border thickness
borderThickness = 10





# Ask the user to enter the labels
labels = []
label = input("Enter the labels (one per line, press enter on an empty line to finish): \n")
while label != "":
    labels.append(label)
    label = input()

# Set the font
font = ImageFont.truetype("segoeuib.ttf", fontSize)





# Generate the images
for i, label in enumerate(labels):
    # Calculate the size of the image
    labelWidth, labelHeight = font.getsize(label)
    labelWidth += 10 + 3*borderThickness

    # Create the image
    image = Image.new('RGBA', (labelWidth, font.getsize("|")[1]), (0, 0, 0, 0))

    # Draw the text
    draw = ImageDraw.Draw(image)
    draw.text((5+borderThickness, -labelHeight/16), label, font=font, fill=(0, 0, 0, 255))

    # Draws a 3px thick black rectangle around the text
    draw.rectangle([(0, 0), (labelWidth - borderThickness, font.getsize("|")[1]-borderThickness)], outline=(0, 0, 0, 255), width=borderThickness)

    # Save the image
    image.save(os.path.join(labelDirectory, str(i) + ".png"))





# Stitch the labels together
# Get the list of PNG images in the input directory
images = [Image.open(os.path.join(labelDirectory, f)) for f in os.listdir(labelDirectory) if f.endswith('.png')]

# Set the maximum width of a line
maxWidth = 2048

areAllLabelsStitched = False

while not(areAllLabelsStitched):
    currentWidth = 0
    imageLine = Image.new('RGBA', (maxWidth, images[0].size[1]), (0, 0, 0, 0))

    # Create the label lines one by one
    while currentWidth < maxWidth:
        # Get the next label
        if len(images) > 0:
            image = images.pop(0)
        else:
            areAllLabelsStitched = True
            break

        # Calculate the size of the image
        labelWidth, labelHeight = image.size

        # If the label is too big, skip it
        if labelWidth > maxWidth:
            continue

        # If the label is too big for the current line, skip it
        if currentWidth + labelWidth > maxWidth:
            images.insert(0, image)
            break

        # Add the label to the current line
        currentWidth += labelWidth

        # Paste the label in the current line
        imageLine.paste(image, (currentWidth - labelWidth, 0))

    # Save the label line
    imageLine.save(os.path.join(labelLinesDirectory, str(len(os.listdir(labelLinesDirectory))) + ".png"))





# Stitch the label lines together
# Get the list of PNG images in the input directory
images = [Image.open(os.path.join(labelLinesDirectory, f)) for f in os.listdir(labelLinesDirectory) if f.endswith('.png')]

# Calculate the size of the output image
totalLabelHeight = sum([image.size[1] for image in images])

# Create the output image
outputImage = Image.new('RGBA', (maxWidth, totalLabelHeight), (0, 0, 0, 0))
currentHeight = 0

for i, image in enumerate(images):

    # Calculate the size of the image
    labelWidth, labelHeight = image.size

    # Paste the input images into the output image
    outputImage.paste(image, (0,currentHeight))

    currentHeight += labelHeight

# Determine the number of the output image already generated
i = 0
while os.path.exists(os.path.join(outputDirectory, 'labels.' + str(i) + '.png')):
    i += 1

# Save the output image
outputImage.save(os.path.join(outputDirectory, 'labels.' + str(i) + '.png'))
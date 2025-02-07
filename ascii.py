from PIL import Image
import requests

imageLink = requests.get('https://api.thecatapi.com/v1/images/search').json()[0]['url']
imageData = requests.get(imageLink).content
with open('input_1.png', 'wb') as handler:
    handler.write(imageData)

# GRAYSCALE & DOWNSCALE IMAGE
img = Image.open('input_1.png').convert('L')
base_width = 100 # width of image
aspect_ratio = 2 # squish
wpercent = (base_width / float(img.size[0]))
hsize = int((float(img.size[1]) * float(wpercent)) / aspect_ratio)
img = img.resize((base_width, hsize), Image.Resampling.LANCZOS) # resize
img.save('grayscaled_input.png')

# GET IMAGE DIMENSIONS AND CONVERT INTO LISTS OF VALUES
pixels = list(img.getdata())
width, height = img.size
values_by_row = [pixels[i * width:(i + 1) * width] for i in range(height)] # takes just the value from each pixel

# CONVERT TO CHARACTER BASED ON VALUE
# (reverse for dark font on light background)
thresholds = {
    230: "#",  # lightest areas
    200: "%",
    160: "+",
    120: "-",
    80: ":",
    40: ",",
    0: " ",  # darkest areas
}

for i, x in enumerate(values_by_row): # loop through the rows of the image
  for j, y in enumerate(x): # loop through the pixels in that row
    for thresh in list(thresholds.keys()): # loop through the threshold dictionary
      if y >= thresh: # check whether the pixel meets the threshold
        values_by_row[i][j] = thresholds[thresh] # replace it with the character if it does
        break

for x in values_by_row:
  print("".join(x))
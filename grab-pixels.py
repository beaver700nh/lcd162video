from PIL import Image
from sys import argv, exit, stdout
from functools import reduce

if len(argv) < 6:
  print("Not enough arguments!")
  exit()

_, img_in, text_out, sector, thres, invert = argv
sector = int(sector)
thres = int(thres)
invert = invert == "invert"

print(f"Converting {img_in} to {text_out} at sector {sector}?")
print(f": Black/white threshold = {thres}, Invert colors = {invert}")

# if input() != "yes":
#   exit()

img = Image.open(img_in)

if img.mode != "L":
  print(f"Image must be grayscale, not {img.mode}.")
  exit()

data = img.tobytes()

W, H = img.size

def pprint(arr, w):
  for i, n in enumerate(arr):
    print(f"{n:02X} ", end=("" if (i + 1) % w != 0 else "\n"))

# pprint(data, W)

data = list(map(lambda n: int(invert ^ (n > thres)), data))

def squeezed(arr, group_size):
  grouped = [arr[i : i+group_size] for i in range(0, len(arr), group_size)]
  squeezer = lambda group: reduce(lambda acc, val: acc << 1 | val, group)

  return list(map(squeezer, grouped))

data = squeezed(data, 5)

def rearranged(arr, w, h):
  out = []
  for chunk in range(0, len(arr), w * h):
    for i in range(w):
      out.extend(arr[chunk + i : chunk + i + h * w : w])

  return out

data = rearranged(data, W // 5, 8)

# pprint(data, 8)

LINE_LEN = 2 + 6 * 8 # 2 for indentation, 6 per byte, 8 bytes

def output(file):
  file.write(" " * LINE_LEN + f" // sector {sector:08d}, === start\n")               # Marker - Sector start

  for row in range(H // 8):
    file.write(" " * LINE_LEN + f" // sector {sector:08d}, line {row:03d}\n")        # Marker - Line tag

    for col in range(W // 5):
      file.write("  ")                                                               # Indentation

      for i in range(8):
        val = data[i + (col + row * W//5) * 8]
        file.write(f"0x{val:02X}, ")                                                 # Element

      file.write(f" // sector {sector:08d}, line {row:03d}, character {col:03d}\n")  # Marker - Character tag

  file.write(" " * LINE_LEN + f" // sector {sector:08d}, === end\n")                 # Marker - Sector end

with open(text_out, "a") as the_file:
  output(the_file)

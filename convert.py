import cv2
import sys

if len(sys.argv) < 5:
  print("Not enough arguments!")
  sys.exit()

FPS_I = int(sys.argv[3])
FPS_O = int(sys.argv[4])

RATIO = FPS_I / FPS_O

print(f"Converting video {sys.argv[1]} @ {FPS_I} to {sys.argv[2]}frame-n.png @ {FPS_O}?")

if not input() == "yes":
  sys.exit()

capt = cv2.VideoCapture(sys.argv[1])

i = 0
j = 0

while capt.isOpened():
  ret, frame = capt.read()

  if not ret:
    break

  temp = i % RATIO
  if temp <= 0.5 or temp > (RATIO - 0.5):
    cv2.imwrite(sys.argv[2] + f"frame-{j:08d}.png", frame)
    j += 1

  i += 1

capt.release()
cv2.destroyAllWindows()

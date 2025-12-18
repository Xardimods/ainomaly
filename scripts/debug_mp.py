import mediapipe
print(dir(mediapipe))
try:
    import mediapipe.python.solutions as solutions
    print("Found mediapipe.python.solutions")
except ImportError:
    print("Could not import mediapipe.python.solutions")

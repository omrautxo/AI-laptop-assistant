import face_recognition

# Load your image
my_image = face_recognition.load_image_file("om_face.jpg")  # <-- your face photo
my_face_encoding = face_recognition.face_encodings(my_image)[0]

# Save in a list
known_face_encodings = [my_face_encoding]
known_face_names = ["Om (Bossman)"]

import os
from facenet_pytorch import InceptionResnetV1, MTCNN
from PIL import Image
import torch

REFERENCE_DIR = "reference_photos"
EMBEDDINGS_DIR = "embeddings"

os.makedirs(EMBEDDINGS_DIR, exist_ok=True)

mtcnn = MTCNN(image_size=160, margin=0, keep_all=True)
model = InceptionResnetV1(pretrained='vggface2').eval()


def process_and_save_embedding(image_path):
    img = Image.open(image_path)
    faces = mtcnn(img, return_prob=False)

    if faces is None or len(faces) == 0:
        print("No faces detected.")
        return "❌ No face detected"

    if isinstance(faces, torch.Tensor):
        print(f"Detected {faces.shape[0]} face(s).")
        for i in range(faces.shape[0]):
            face = faces[i]
            embedding = model(face.unsqueeze(0))
            filename = os.path.splitext(os.path.basename(image_path))[0] + f"_{i}" + ".pt"
            torch.save(embedding, os.path.join(EMBEDDINGS_DIR, filename))
            print(f"Saved embedding for {image_path} as {filename}")


if __name__ == "__main__":
    for fname in os.listdir(REFERENCE_DIR):
        if fname.lower().endswith((".jpg", ".jpeg", ".png")):
            process_and_save_embedding(os.path.join(REFERENCE_DIR, fname))

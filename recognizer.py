import torch
from facenet_pytorch import MTCNN, InceptionResnetV1
from PIL import Image
import os

# Initialize MTCNN with multi-face support
mtcnn = MTCNN(image_size=160, margin=0, keep_all=True)
model = InceptionResnetV1(pretrained='vggface2').eval()

# Load known embeddings
EMBEDDINGS_DIR = 'embeddings'
known_embeddings = []

for fname in os.listdir(EMBEDDINGS_DIR):
    if fname.endswith('.pt'):
        emb = torch.load(os.path.join(EMBEDDINGS_DIR, fname))
        known_embeddings.append(emb)

print(f"Loaded {len(known_embeddings)} known embeddings.")


def recognize_faces(image_path: str, threshold=0.8) -> str:
    img = Image.open(image_path).convert("RGB")
    faces = mtcnn(img, return_prob=False)

    if faces is None or len(faces) == 0:
        print("No faces detected.")
        return "❌ No face detected"

    # Ensure we always work with a list of faces
    if isinstance(faces, torch.Tensor):
        print(f"Detected {faces.shape[0]} face(s).")
        for i in range(faces.shape[0]):
            face = faces[i]
            if face.shape[0] != 3:
                print(f"Skipping face {i + 1} due to invalid shape: {face.shape}")
                continue

            embedding = model(face.unsqueeze(0))
            for known_emb in known_embeddings:
                dist = (embedding - known_emb).norm().item()
                if dist < threshold:
                    print(f"✅ Match found on face {i + 1} - Distance: {dist:.4f}")
                    return "✅ Match found"

        print(f"❌ No match found in {faces.shape[0]} face(s).")
        return "❌ No match found"

    # Handle case where faces is a list
    print(f"Detected {len(faces)} face(s).")
    for i, face in enumerate(faces):
        if face.shape[0] != 3:
            print(f"Skipping face {i + 1} due to invalid shape: {face.shape}")
            continue

        embedding = model(face.unsqueeze(0))
        for known_emb in known_embeddings:
            dist = (embedding - known_emb).norm().item()
            if dist < threshold:
                print(f"✅ Match found on face {i + 1} - Distance: {dist:.4f}")
                return "✅ Match found"

    print(f"❌ No match found in {len(faces)} face(s).")
    return "❌ No match found"

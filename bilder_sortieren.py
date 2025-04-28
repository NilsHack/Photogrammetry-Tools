import cv2
import os
import shutil
from PIL import Image
import imagehash
from tqdm import tqdm

# Pfade festlegen
source_folder = r"C:\Users\Nils\Pictures\Labor_Demo\Camera"
rohvideos_folder = os.path.join(source_folder, "Rohvideos")
bilder_folder = os.path.join(source_folder, "GeprüfteBilder")
duplicates_folder = os.path.join(source_folder, "duplicates")

# Ordner anlegen
os.makedirs(bilder_folder, exist_ok=True)
os.makedirs(duplicates_folder, exist_ok=True)

# Schärfe- & Ähnlichkeits-Schwellen
BLUR_THRESHOLD = 20.0
HASH_DIFF_THRESHOLD = 8

def ist_unscharf_mitte(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    h, w = gray.shape
    x_start = int(w * 0.375)
    y_start = int(h * 0.375)
    x_end = int(w * 0.625)
    y_end = int(h * 0.625)
    mitte = gray[y_start:y_end, x_start:x_end]
    return cv2.Laplacian(mitte, cv2.CV_64F).var() < BLUR_THRESHOLD

def videos_in_scharfe_bilder_umwandeln():
    video_extensions = [".mp4", ".mov", ".avi", ".mkv"]
    dateien = [f for f in os.listdir(rohvideos_folder) if os.path.splitext(f)[1].lower() in video_extensions]

    for file in tqdm(dateien, desc="Videos konvertieren & unscharfe löschen"):
        filepath = os.path.join(rohvideos_folder, file)
        cap = cv2.VideoCapture(filepath)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames == 0:
            print(f"⚠️ Keine Frames in {file}, überspringe.")
            cap.release()
            continue

        frame_number = 0
        saved_count = 0

        with tqdm(total=total_frames, desc=f"Verarbeite {file}", unit="Frame") as pbar:
            while True:
                success, frame = cap.read()
                if not success:
                    break

                if not ist_unscharf_mitte(frame):
                    bild_name = f"{os.path.splitext(file)[0]}_Sharp_{frame_number:05}.png"
                    cv2.imwrite(os.path.join(bilder_folder, bild_name), frame)
                    saved_count += 1

                frame_number += 1
                pbar.update(1)

        cap.release()
        print(f"✅ {file}: {saved_count} scharfe Bilder gespeichert.")

def ist_aehnliches_bild(image1_hash, gesehen_hashes, threshold):
    return any(abs(image1_hash - saved_hash) <= threshold for saved_hash in gesehen_hashes)

def aehnliche_bilder_finden_und_verschieben():
    bilder_liste = sorted([f for f in os.listdir(bilder_folder) if f.lower().endswith(".png")])
    gesehen_hashes = []
    count_duplikat = 1
    count_scharf = 1

    for filename in tqdm(bilder_liste, desc="Ähnliche Bilder filtern"):
        filepath = os.path.join(bilder_folder, filename)

        try:
            image = Image.open(filepath)
            image_hash = imagehash.phash(image)

            if ist_aehnliches_bild(image_hash, gesehen_hashes, HASH_DIFF_THRESHOLD):
                neuer_name = f"threshold_{HASH_DIFF_THRESHOLD}_failed_duplicate_{count_duplikat:05}.png"
                shutil.move(filepath, os.path.join(duplicates_folder, neuer_name))
                count_duplikat += 1
            else:
                neuer_name = f"threshold_{HASH_DIFF_THRESHOLD}_pass_sortiert_{count_scharf:05}.png"
                os.rename(filepath, os.path.join(bilder_folder, neuer_name))
                gesehen_hashes.append(image_hash)
                count_scharf += 1

        except Exception as e:
            print(f"❌ Fehler bei {filename}: {e}")

if __name__ == "__main__":
    try:
        aehnliche_bilder_finden_und_verschieben()
        print("🎉 Verarbeitung abgeschlossen!")
    except Exception as e:
        print(f"💥 Fehler im Ablauf: {e}")

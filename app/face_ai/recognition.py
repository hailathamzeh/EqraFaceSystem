"""Face registration, recognition, and removal helpers.

The module keeps the original public API used by ``UserInterface.py`` while
making runtime paths independent of the caller's current working directory.
"""

import argparse
import json
import sys
from pathlib import Path

import face_recognition
import numpy as np
from PIL import Image


DEFAULT_ID_FOLDER = Path(__file__).resolve().parent / "id_folder"


def _id_folder_path(id_folder):
    folder = Path(id_folder or DEFAULT_ID_FOLDER).expanduser().resolve()
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _uses_default_cpu(used_cpu):
    if used_cpu == "yes":
        return False
    try:
        return int(used_cpu) < 1
    except (TypeError, ValueError):
        return True


def _json_result(payload):
    result = json.dumps(payload)
    print(result)
    return result


def _exit_json(payload):
    _json_result(payload)
    raise SystemExit(2)


def generate_id(image_path, id, used_cpu, id_folder):
    try:
        folder = _id_folder_path(id_folder)
        image = face_recognition.load_image_file(image_path)
        encodings = face_recognition.face_encodings(image)
        if not encodings:
            _json_result({"err": "no features detected"})
            return False

        np.savetxt(folder / f"{id}.txt", encodings[0], fmt="%f")
        payload = {"ok": "face and ID saved"}
        if _uses_default_cpu(used_cpu):
            payload["warning"] = "the default number of CPUs will be used"
        _json_result(payload)
        return True
    except Exception:
        _json_result({"err": "no features detected"})
        return False


def detect_id(image_path, tol, used_cpu, id_folder):
    folder = _id_folder_path(id_folder)
    encoding_files = sorted(folder.glob("*.txt"))
    if not encoding_files:
        return _json_result(
            {"err": "there is no face data stored", "data": [{"id": "Unknown"}]}
        )

    known_face_encodings = []
    known_face_names = []
    for encoding_file in encoding_files:
        try:
            known_face_encodings.append(np.loadtxt(encoding_file, dtype=float))
            known_face_names.append(encoding_file.stem)
        except (OSError, ValueError):
            continue

    if not known_face_encodings:
        return _json_result(
            {"err": "there is no valid face data stored", "data": [{"id": "Unknown"}]}
        )

    unknown_image = face_recognition.load_image_file(image_path)
    face_locations = face_recognition.face_locations(unknown_image)
    face_encodings = face_recognition.face_encodings(unknown_image, face_locations)

    data = []
    for face_encoding in face_encodings:
        matches = face_recognition.compare_faces(
            known_face_encodings,
            face_encoding,
            tolerance=float(tol),
        )
        face_distances = face_recognition.face_distance(
            known_face_encodings,
            face_encoding,
        )
        best_match_index = int(np.argmin(face_distances))
        name = (
            known_face_names[best_match_index]
            if matches[best_match_index]
            else "Unknown"
        )

        # Kept as ``accuracy`` for compatibility with the original UI output.
        # This value is the closest face distance multiplied by 100.
        data.append(
            {
                "id": name,
                "accuracy": round(float(face_distances[best_match_index]) * 100, 3),
                "tolerance": float(tol),
            }
        )

    if not data:
        data = [{"id": "Unknown"}]

    payload = {"data": data}
    if _uses_default_cpu(used_cpu):
        payload["warning"] = "the default number of CPUs will be used"
    return _json_result(payload)


def del_id(id, id_folder):
    encoding_file = _id_folder_path(id_folder) / f"{id}.txt"
    try:
        encoding_file.unlink()
        _json_result({"ok": f"id {id} removed"})
        return True
    except FileNotFoundError:
        _json_result({"err": f"id {id} is not in the database"})
        return False


def _valid_image(path):
    try:
        with Image.open(path) as image:
            image.verify()
        return True
    except (OSError, ValueError):
        return False


def main():
    parser = argparse.ArgumentParser(description="Face-recognition commands")
    parser.add_argument("--mode", choices=("new", "detect", "del"))
    parser.add_argument("--image_path", help="Path to an input image")
    parser.add_argument("--id", help="Identifier for the person")
    parser.add_argument("--tol", type=float, help="Recognition tolerance")
    parser.add_argument("--cpu", type=int, help="Number of CPUs")
    parser.add_argument(
        "--id_folder",
        default=str(DEFAULT_ID_FOLDER),
        help="Directory used for local face encodings",
    )
    args = parser.parse_args()

    used_cpu = args.cpu if args.cpu is not None else "no"
    if args.mode is None:
        _exit_json({"err": "please provide the mode"})

    if args.mode in ("new", "detect"):
        if args.image_path is None:
            _exit_json({"err": "please provide the image path"})
        if not _valid_image(args.image_path):
            _exit_json({"err": "please provide a correct image path"})

    if args.mode == "new":
        if args.id is None:
            _exit_json({"err": "please provide the id"})
        generate_id(args.image_path, args.id, used_cpu, args.id_folder)
    elif args.mode == "detect":
        if args.tol is None:
            _exit_json({"err": "please add the tolerance argument"})
        detect_id(args.image_path, args.tol, used_cpu, args.id_folder)
    elif args.mode == "del":
        if args.id is None:
            _exit_json({"err": "please provide the id"})
        del_id(args.id, args.id_folder)


if __name__ == "__main__":
    main()

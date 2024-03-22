import shutil
import os
import random
import fitz
import glob
from alive_progress import alive_bar


def find_coordinates(
    pdf_path: str, search_text: str, move_by: int = 20
) -> dict[int : dict[str:int]]:
    pdf = fitz.open(pdf_path)
    coords = {}

    for page_num, page in enumerate(pdf):
        text_instances = page.search_for(search_text)

        for text_instance in text_instances:
            coords.update(
                {
                    page_num: {
                        "x0": int(text_instance.x0) + move_by,
                        "y0": int(text_instance.y0),
                        "x1": int(text_instance.x1) + move_by,
                        "y1": int(text_instance.y1),
                    }
                }
            )

    return coords


def get_random_sign(path) -> str:
    random_signs = glob.glob(path)
    if not random_signs:
        raise ValueError(f"No subsigns found in ${path}")

    return random.choice(random_signs)


def creaete_tmp_copies(pdfs: list, tmp_path: str) -> list[str]:
    create_folder_if_not_exisists(tmp_path)

    print("Creating temorary files...")
    with alive_bar(len(pdfs)) as bar:
        for pdf in pdfs:
            shutil.copyfile(pdf, os.path.join(tmp_path, os.path.basename(pdf)))
            bar()

    return glob.glob(os.path.join(tmp_path, "*.pdf"))


def create_folder_if_not_exisists(folder_path: str) -> None:
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)


def sign_pdf(
    pdf: str,
    main_sign_path: str,
    sub_sign_path: str,
    main_coordinates,
    sub_coordinates,
    width: int | float,
    height: int | float,
    output_path: str,
) -> None:
    with fitz.open(pdf) as f:
        for page_num, page in enumerate(f):
            main_coords = main_coordinates[page_num]
            sub_coords = sub_coordinates[page_num]
            random_sub_sign = get_random_sign(sub_sign_path)
            add_img_to_file(page, main_coords, width, height, main_sign_path)
            add_img_to_file(page, sub_coords, width, height, random_sub_sign)

        f.ez_save(output_path)


def add_img_to_file(
    page: any,
    coordinates: dict["x0":int, "y0":int],
    width: int,
    height: int,
    sign_path: str,
) -> None:
    x0 = coordinates["x0"]
    y0 = coordinates["y0"]
    sign = (x0, y0, x0 + width, y0 + height)
    page.insert_image(sign, filename=sign_path)


def sign_and_save_pdf(pdfs: list, output_path: str) -> None:
    main_sign_txt = "Kontrolle wurde durchgeführt"
    subsign_text = "Stellen / Verblistern wurde durchgeführt von"
    main_sings_path = os.path.join(os.getcwd(), "data", "signs", "main_sign")
    main_signs = glob.glob(os.path.join(main_sings_path, "*.png"))

    if not main_signs:
        raise ValueError(f"No main sing found in ${main_sings_path}")
    main_sign = main_signs[0]

    print("Signing pdfs...")
    with alive_bar(len(pdfs)) as bar:
        for pdf in pdfs:
            main_sign_coords = find_coordinates(pdf, main_sign_txt)
            subsign_coords = find_coordinates(pdf, subsign_text)
            sub_sign = os.path.join(
                os.getcwd(), "data", "signs", "random_signs", "*.png"
            )
            pdf_output_path = os.path.join(output_path, os.path.basename(pdf))
            sign_pdf(
                pdf,
                main_sign,
                sub_sign,
                main_sign_coords,
                subsign_coords,
                50,
                50,
                pdf_output_path,
            )
            bar()
    print("Done!")


def remove_tmp_files(path) -> None:
    # Iterate over the files and subdirectories in the folder
    for file_name in os.listdir(path):
        file_path = os.path.join(path, file_name)
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)
        else:
            # Remove the subdirectory recursively
            shutil.rmtree(file_path)

    # Remove the empty folder
    os.rmdir(path)


def main():
    pdfs_path = os.path.join(os.getcwd(), "*.pdf")
    signed_pdfs_path = os.path.join(os.getcwd(), "signed")
    tmp_path = os.path.join(os.getcwd(), "tmp_pdfs_folder")

    pdfs = glob.glob(pdfs_path)
    if not pdfs:
        raise ValueError(f"No pdfs found in ${pdfs_path}")

    pdf_copies = creaete_tmp_copies(pdfs, tmp_path)
    create_folder_if_not_exisists(signed_pdfs_path)
    sign_and_save_pdf(pdf_copies, signed_pdfs_path)
    remove_tmp_files(tmp_path)


if __name__ == "__main__":
    main()

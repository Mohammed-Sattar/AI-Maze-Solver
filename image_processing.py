from PIL import Image
import numpy as np

# width, height = Image.open("maze2.gif").size

# new_width = round(width / 4)
# new_height = round(height / 4)

def image_to_matrix(image__path, threshold=128, new_width=50, new_height=30):

    width, height = Image.open(image__path).size

    new_width = round(width / 4)
    new_height = round(height / 4)

    img = Image.open(image__path)
    img = img.resize((new_width, new_height))
    gray_img = img.convert("L")
    # Binarize using threshold
    binary_img = gray_img.point(lambda x: 0 if x < threshold else 1)
    # Convert to numpy array for matrix representation
    binary_matrix = np.array(binary_img)
    save_matrix_to_txt(binary_matrix, "output_matrix.txt")
    return binary_matrix


def save_matrix_to_txt(matrix, filename):
    with open(filename, "w") as f:
        f.write("[\n")  # Start 2D array
        for row in matrix:
            line = "[" + ",".join(map(str, row)) + "],\n"
            f.write(line)
        f.write("]\n")  # End 2D array


# image_path = "SmallMaze.jpg"
image_path = "GUI Mohammed\smallMaze.gif"
matrix = image_to_matrix(image_path)
save_matrix_to_txt(matrix, "GUI Mohammed\output_matrix.txt")

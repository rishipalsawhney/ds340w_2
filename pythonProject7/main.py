# import os
# import requests
# import cv2
# import numpy as np
#
#
# # Function to download the dataset
# def download_dataset(url, save_dir):
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#
#     filename = url.split('/')[-1]
#
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(os.path.join(save_dir, filename), 'wb') as f:
#             f.write(response.content)
#         print(f"Downloaded dataset successfully: {filename}")
#     else:
#         print("Failed to download dataset.")
#
#
# # Function to perform license plate detection
# def detect_license_plate(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 100, 200)
#     contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
#
#     for contour in contours:
#         perimeter = cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
#
#         if len(approx) == 4:
#             license_plate = approx
#             break
#
#     cv2.drawContours(image, [license_plate], -1, (0, 255, 0), 2)
#
#     return image, license_plate
#
#
# # Function to perform character segmentation
# def segment_characters(image, license_plate):
#     (x, y, w, h) = cv2.boundingRect(license_plate)
#     plate = image[y:y + h, x:x + w]
#     gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     characters = []
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         if w / h > 0.3 and w / h < 1.5 and h > 10:
#             character = thresh[y:y + h, x:x + w]
#             characters.append(character)
#
#     return characters
#
#
# # Main function
# def main():
#     # Download the dataset
#     dataset_url = "https://makeml.app/datasets/cars-license-plates"
#     save_directory = "./car_license_plates_dataset"
#     download_dataset(dataset_url, save_directory)
#
#     # Process the downloaded images
#     for root, dirs, files in os.walk(save_directory):
#         for file in files:
#             if file.endswith(".jpg") or file.endswith(".png"):
#                 image_path = os.path.join(root, file)
#                 image = cv2.imread(image_path)
#                 detected_image, license_plate = detect_license_plate(image)
#                 characters = segment_characters(detected_image, license_plate)
#
#                 # Display the segmented characters
#                 for i, character in enumerate(characters):
#                     cv2.imshow(f"Character {i}", character)
#                 # Display the detected license plate
#                 cv2.imshow("Detected License Plate", detected_image)
#                 cv2.waitKey(0)
#                 cv2.destroyAllWindows()
#
#
# if __name__ == "__main__":
#     main()


# import os
# import requests
# import cv2
# import numpy as np
# import csv
#
#
# # Function to download the dataset
# def download_dataset(url, save_dir):
#     if not os.path.exists(save_dir):
#         os.makedirs(save_dir)
#
#     filename = url.split('/')[-1]
#
#     response = requests.get(url)
#     if response.status_code == 200:
#         with open(os.path.join(save_dir, filename), 'wb') as f:
#             f.write(response.content)
#         print(f"Downloaded dataset successfully: {filename}")
#     else:
#         print("Failed to download dataset.")
#
#
# # Function to perform license plate detection
# def detect_license_plate(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 100, 200)
#     contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
#
#     for contour in contours:
#         perimeter = cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
#
#         if len(approx) == 4:
#             license_plate = approx
#             break
#
#     cv2.drawContours(image, [license_plate], -1, (0, 255, 0), 2)
#
#     return image, license_plate
#
#
# # Function to perform character segmentation
# def segment_characters(image, license_plate):
#     (x, y, w, h) = cv2.boundingRect(license_plate)
#     plate = image[y:y + h, x:x + w]
#     gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     characters = []
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         if w / h > 0.3 and w / h < 1.5 and h > 10:
#             character = thresh[y:y + h, x:x + w]
#             characters.append(character)
#
#     return characters
#
#
# # Function to save detected characters to a CSV file
# def save_to_csv(characters, csv_filename):
#     with open(csv_filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Character'])
#         for character in characters:
#             flattened_character = character.flatten()
#             character_string = ''.join(map(str, flattened_character))
#             writer.writerow([character_string])
#
#
# # Main function
# def main():
#     # Download the dataset
#     dataset_url = "https://makeml.app/datasets/cars-license-plates"
#     save_directory = "./car_license_plates_dataset"
#     download_dataset(dataset_url, save_directory)
#
#     # Create CSV file
#     csv_filename = "license_plate_characters.csv"
#
#     # Process the downloaded images
#     for root, dirs, files in os.walk(save_directory):
#         for file in files:
#             if file.endswith(".jpg") or file.endswith(".png"):
#                 image_path = os.path.join(root, file)
#                 image = cv2.imread(image_path)
#                 detected_image, license_plate = detect_license_plate(image)
#                 characters = segment_characters(detected_image, license_plate)
#
#                 # Save detected characters to CSV file
#                 save_to_csv(characters, csv_filename)
#
#
# if __name__ == "__main__":
#     main()

# import os
# import cv2
# import numpy as np
# import csv
#
#
# # Function to perform license plate detection
# def detect_license_plate(image):
#     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
#     edges = cv2.Canny(gray, 100, 200)
#     contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]
#
#     for contour in contours:
#         perimeter = cv2.arcLength(contour, True)
#         approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
#
#         if len(approx) == 4:
#             license_plate = approx
#             break
#
#     cv2.drawContours(image, [license_plate], -1, (0, 255, 0), 2)
#
#     return image, license_plate
#
#
# # Function to perform character segmentation
# def segment_characters(image, license_plate):
#     (x, y, w, h) = cv2.boundingRect(license_plate)
#     plate = image[y:y + h, x:x + w]
#     gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
#     _, thresh = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY_INV)
#     contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#
#     characters = []
#     for contour in contours:
#         (x, y, w, h) = cv2.boundingRect(contour)
#         if w / h > 0.3 and w / h < 1.5 and h > 10:
#             character = thresh[y:y + h, x:x + w]
#             characters.append(character)
#
#     return characters
#
#
# # Function to save detected characters to a CSV file
# def save_to_csv(characters, csv_filename):
#     with open(csv_filename, mode='a', newline='') as file:
#         writer = csv.writer(file)
#         writer.writerow(['Character'])
#         for character in characters:
#             flattened_character = character.flatten()
#             character_string = ''.join(map(str, flattened_character))
#             writer.writerow([character_string])
#
#
# # Main function
# def main():
#     # Path to the images folder within the project folder
#     images_folder = "/Users/rishisawhney/Downloads/pytorch-unsupervised-segmentation-tip-master/images"
#     # Create CSV file
#     csv_filename = "license_plate_characters.csv"
#
#     # Process the images
#     for filename in os.listdir(images_folder):
#         if filename.endswith(".jpg") or filename.endswith(".png"):
#             image_path = os.path.join(images_folder, filename)
#             image = cv2.imread(image_path)
#             detected_image, license_plate = detect_license_plate(image)
#             characters = segment_characters(detected_image, license_plate)
#
#             # Save detected characters to CSV file
#             save_to_csv(characters, csv_filename)
#
#
# if __name__ == "__main__":
#     main()


import os
import cv2
import numpy as np
import csv


# Function to perform license plate detection
def detect_license_plate(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 100, 200)
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:10]

    license_plate = None  # Initialize license_plate variable

    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)

        if len(approx) == 4:
            license_plate = approx
            break

    if license_plate is not None:
        cv2.drawContours(image, [license_plate], -1, (0, 255, 0), 2)

    return image, license_plate


# Function to perform character segmentation
def segment_characters(image, license_plate):
    if license_plate is None:
        return []  # Return empty list if no license plate is detected

    (x, y, w, h) = cv2.boundingRect(license_plate)
    plate = image[y:y + h, x:x + w]
    gray_plate = cv2.cvtColor(plate, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray_plate, 150, 255, cv2.THRESH_BINARY_INV)
    contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    characters = []
    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        if w / h > 0.3 and w / h < 1.5 and h > 10:
            character = thresh[y:y + h, x:x + w]
            characters.append(character)

    return characters


# Function to save detected characters to a CSV file
def save_to_csv(characters, csv_filename):
    with open(csv_filename, mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['Character'])
        for character in characters:
            flattened_character = character.flatten()
            character_string = ''.join(map(str, flattened_character))
            writer.writerow([character_string])


# Main function
def main():
    # Path to the images folder within the project folder
    images_folder = "images"
    # Create CSV file
    csv_filename = "license_plate_characters.csv"

    # Process the images
    for filename in os.listdir(images_folder):
        if filename.endswith(".jpg") or filename.endswith(".png"):
            image_path = os.path.join(images_folder, filename)
            image = cv2.imread(image_path)
            detected_image, license_plate = detect_license_plate(image)

            # Check if license plate is detected
            if license_plate is not None:
                characters = segment_characters(detected_image, license_plate)

                # Save detected characters to CSV file
                save_to_csv(characters, csv_filename)
            else:
                print(f"License plate not detected for image: {filename}")

                # Print contours for debugging
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                for contour in contours:
                    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
                cv2.imshow("Contours", image)
                cv2.waitKey(0)
                cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

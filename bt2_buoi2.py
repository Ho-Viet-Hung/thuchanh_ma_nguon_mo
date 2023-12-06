import cv2
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk

selected_filter = None
brightness_factor = 1.0
img = None
smoothing_factor = 0.5

start_x, start_y, end_x, end_y = 0, 0, 0, 0  # Initialize variables for region selection
is_drawing = False
selected_region = None

def apply_filter(filter_type):
    global img, selected_filter, brightness_factor
    if img is not None:
        if filter_type == "sharpen_1":
            kernel = np.array([[-1, -1, -1], [-1, 9, -1], [-1, -1, -1]])
        elif filter_type == "sharpen_2":
            kernel = np.array([[1, 1, 1], [1, -7, 1], [1, 1, 1]])
        elif filter_type == "sharpen_3":
            kernel = np.array([[-1, -1, -1, -1, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, 2, 8, 2, -1],
                               [-1, 2, 2, 2, -1],
                               [-1, -1, -1, -1, -1]]) / 8.0
        else:
            kernel = np.array([[0, 0, 0], [0, 1, 0], [0, 0, 0]])

        output = cv2.filter2D(img, -1, kernel)
        output = apply_brightness(output, brightness_factor)
        cv2.imshow('Filtered Image', output)
        selected_filter = filter_type

def apply_effect(effect_type):
    global img, selected_filter, brightness_factor
    if img is not None:
        if effect_type == "grayscale":
            output = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        elif effect_type == "invert_colors":
            output = cv2.bitwise_not(img)
        else:
            output = img

        output = apply_brightness(output, brightness_factor)
        cv2.imshow('Filtered Image', output)
        selected_filter = effect_type

def apply_brightness(image, factor):
    return cv2.convertScaleAbs(image, alpha=factor, beta=0)

def save_image():
    global img
    if img is not None:
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG files", "*.jpg")])
        if file_path:
            cv2.imwrite(file_path, img)
            print("Image saved successfully")

def open_image():
    global img
    file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png *.bmp *.gif *.tif")])
    if file_path:
        img = cv2.imread(file_path)
        if img is not None:
            cv2.imshow('Original', img)
            apply_filter(selected_filter)

def update_brightness(value):
    global brightness_factor
    brightness_factor = float(value)
    apply_filter(selected_filter)

def select_region(event, x, y, flags, param):
    global start_x, start_y, end_x, end_y, is_drawing, img, selected_region

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        is_drawing = True
    elif event == cv2.EVENT_MOUSEMOVE:
        if is_drawing:
            end_x, end_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        is_drawing = False
        end_x, end_y = x, y

        cv2.rectangle(img, (start_x, start_y), (end_x, end_y), (0, 255, 0), 2)

        selected_region = img[start_y:end_y, start_x:end_x]

def update_smoothing_factor(*args):
    global smoothing_factor
    smoothing_factor = smoothing_slider.get()
    if selected_region is not None:
        on_ok_button_click()

def on_ok_button_click():
    global img, selected_region, smoothing_factor
    if selected_region is not None and selected_region.shape[0] > 0 and selected_region.shape[1] > 0:
        kernel_size = int(smoothing_factor * 10) + 1
        kernel = np.ones((kernel_size, kernel_size), np.float32) / (kernel_size ** 2)
        smoothed_region = cv2.filter2D(selected_region, -1, kernel)
        img[start_y:end_y, start_x:end_x] = smoothed_region
        cv2.imshow('Portrait with Smoothing', img)

root = tk.Tk()
root.title("Image Filters, Effects, and Smoothing")

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

save_button = tk.Button(root, text="Save Image", command=save_image)
save_button.pack()

sharpen_1_button = tk.Button(root, text="Sharpen 1", command=lambda: apply_filter("sharpen_1"))
sharpen_1_button.pack()

sharpen_2_button = tk.Button(root, text="Sharpen 2", command=lambda: apply_filter("sharpen_2"))
sharpen_2_button.pack()

sharpen_3_button = tk.Button(root, text="Sharpen 3", command=lambda: apply_filter("sharpen_3"))
sharpen_3_button.pack()

grayscale_button = tk.Button(root, text="Grayscale", command=lambda: apply_effect("grayscale"))
grayscale_button.pack()

invert_colors_button = tk.Button(root, text="Invert Colors", command=lambda: apply_effect("invert_colors"))
invert_colors_button.pack()

smoothing_slider = ttk.Scale(root, from_=0, to=1, orient="horizontal", length=200, command=update_smoothing_factor)
smoothing_slider.set(smoothing_factor)
smoothing_slider.pack()

ok_button = tk.Button(root, text="OK", command=on_ok_button_click)
ok_button.pack()

def update():
    key = cv2.waitKey(1)
    if key == 27:
        cv2.destroyAllWindows()
    root.after(1, update)

root.after(1, update)
root.mainloop()

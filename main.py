import serial
import time
import csv
import tkinter as tk
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import messagebox
import threading

data = ""
data1 = []
data2 = []  # New list to store data received through serial

arduino_port = 'COM3'  # Replace with your Arduino's port
baud_rate = 115200  # Match the baud rate set in your Arduino sketch
ser = serial.Serial(arduino_port, baud_rate)

figure, axes = plt.subplots(2, 1)  # Create subplots for two plots

def read_csv_file(file_path):
    data = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            data.extend(row)
    return data

def process_csv():
    global figure, axes

    # Open the file dialog
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])

    # Check if a file was selected
    if file_path:
        global data1

        # Clear the previous plot
        if axes[0] is not None:
            axes[0].cla()  # Clear the axes

        data1 = read_csv_file(file_path)
        #print("Data1")
        #print(data1)

        # Plot the data
        plot_data(data1, axes[0])

    else:
        print("No file selected.")

def plot_data(data, axes):
    # Convert the data to floats
    y_values = [float(x) for x in data]

    # Create the x values
    x_values = list(range(len(y_values)))

    # Plot the data
    axes.cla()
    axes.plot(x_values, y_values)
    axes.set_xlabel('Time', fontsize=10, color='blue')
    axes.set_ylabel('Amplitude', fontsize=10, color='red')
    axes.grid(True)
    plt.subplots_adjust(hspace=0.5)

    figure.canvas.draw()
#
def serial_data():
    result = ', '.join(data1)
    ser.write(str(result).encode())
    #print(result)

        




def read_serial_data():
    global data2

    while True:
        if ser.in_waiting > 0:
            data3 = ser.readline().decode('utf-8', errors='ignore').strip()
            #print(data3)

            # Split the string by commas and convert values to float
            data2 = [str(value) for value in data1]
            #print("Data2")
            #print(data2)

            # Plot the data
            plot_data(data2, axes[1])

        time.sleep(0.01)  # Add a small delay to avoid busy waiting




def main():
    global window
    # Create the GUI window
    window = tk.Tk()

    # Create a button widget to choose the CSV file
    button1 = tk.Button(window, text="Choose CSV File", command=process_csv)
    button1.pack()
    button2 = tk.Button(window, text="Upload", command=serial_data)
    button2.pack()

    canvas = FigureCanvasTkAgg(figure, master=window)
    canvas.get_tk_widget().pack()

    # Create a button widget to upload serial data

    
    serial_thread = threading.Thread(target=read_serial_data)
    serial_thread.daemon = True  # Set the thread as daemon to automatically stop when the main thread exits
    serial_thread.start()
    
    window.geometry("900x700")  # Width x Height

# Alternatively, set a fixed size and disable window resizing
    window.resizable(False, False)

    # Start the GUI event loop
    window.mainloop()

if __name__ == "__main__":
    main()

# Data Communication Functions Visualizer

This Python project uses Tkinter to create a graphical user interface (GUI) that visualizes various data communication functions based on given binary input.

## Features

- User-friendly GUI built with Tkinter
- Input binary data for analysis
- Visualize different data communication functions
- Real-time updates as you input binary data
- Clear and intuitive graphical representation of each encoding method

## Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes pre-installed with Python)
- matplotlib (for plotting graphs)

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/n9e6y/dataCommunicationFunctions.git
   ```
2. Navigate to the project directory:
   ```
   cd dataCommunicationFunctions
   ```
3. Install required dependencies:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the program:
   ```
   python main.py
   ```
2. The GUI will appear. Enter your binary data in the input field.
3. Use the provided buttons or menu options to switch between different visualization modes or to clear the input.

## Project Structure

# Data Communication Functions Visualizer

[Previous content remains unchanged...]

## Project Structure

```
dataCommunicationFunctions/
│
├── encoding_schemes/
│   ├── binary_schemes.py
│   └── modulation_schemes.py
│
├── gui/
│   └── signal_plotter.py
│
├── utils/
│   └── plotting.py
│
├── venv/
│
├── .gitignore
├── main.py
├── README.md
└──  requirements.txt
```

- `encoding_schemes/`: Contains implementations of various encoding and modulation schemes
  - `binary_schemes.py`: Implements binary encoding schemes
  - `modulation_schemes.py`: Implements modulation schemes
- `gui/`: Houses the graphical user interface components
  - `signal_plotter.py`: Manages the plotting of signals in the GUI
- `utils/`: Utility functions and helpers
  - `plotting.py`: Contains helper functions for plotting
- `main.py`: The main entry point of the application
- `requirements.txt`: Lists all the Python dependencies for this project

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Acknowledgments

- Tkinter documentation
- matplotlib library for plotting capabilities

## Troubleshooting

If you encounter any issues with Tkinter, ensure that it's properly installed with your Python distribution. On some Linux systems, you might need to install it separately:

```
sudo apt-get install python3-tk
```

For any other issues or feature requests, please open an issue in this repository.
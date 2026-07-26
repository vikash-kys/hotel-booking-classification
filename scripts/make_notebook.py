import json
import os

with open('model_runner.py', 'r') as f:
    lines = f.readlines()

# Split into chunks based on '# ' or 'print('
cells = []
current_cell = []

for line in lines:
    if line.startswith('print("Generating') or line.startswith('# Prepare') or line.startswith('print("Training'):
        if current_cell:
            cells.append({
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": current_cell
            })
            current_cell = []
    current_cell.append(line)

if current_cell:
    cells.append({
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": current_cell
    })

# Prepend a markdown cell
cells.insert(0, {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "# Hotel Booking Cancellation Prediction\n",
        "\n",
        "This notebook explores the Trivago hotel booking dataset and trains a Random Forest Classifier to predict cancellations."
    ]
})

notebook = {
    "cells": cells,
    "metadata": {
        "kernelspec": {
            "display_name": "Python 3",
            "language": "python",
            "name": "python3"
        }
    },
    "nbformat": 4,
    "nbformat_minor": 4
}

with open('hotel_booking_classification.ipynb', 'w') as f:
    json.dump(notebook, f, indent=2)

print("Notebook generated.")

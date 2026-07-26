# Trivago Hotel Booking Classification

This repository contains a full Data Science portfolio project analyzing the Trivago hotel booking dataset and training a Random Forest Classifier to predict cancellations.

## Project Structure

- `index.html`: The main portfolio website (deployed via GitHub Pages). Contains interactive analysis, visualizations, and code walkthroughs.
- `images/`: The generated static visual assets used in the exploratory data analysis.
- `src/`: The raw Python source code and Jupyter notebook for the machine learning pipeline.
  - `hotel_booking_classification.ipynb`: A Jupyter Notebook containing the full pipeline (EDA, preprocessing, and modeling) that you can run locally.
  - `model_runner.py`: The standalone Python script that performs the exact same pipeline and generates the plot images.
- `scripts/`: Internal utility scripts used to translate the formatting of the HTML files.

## Running Locally

To run the analysis yourself:

1. Clone this repository.
2. Ensure you have `pandas`, `numpy`, `matplotlib`, `seaborn`, and `scikit-learn` installed.
3. Navigate to the `src/` folder and open the `hotel_booking_classification.ipynb` notebook in Jupyter, or run the standalone script:

```bash
python src/model_runner.py
```

## View Live

The analysis is hosted live at: [https://vikash-kys.github.io/hotel-booking-classification/](https://vikash-kys.github.io/hotel-booking-classification/)

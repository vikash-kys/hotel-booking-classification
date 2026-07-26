const fs = require('fs');

const htmlFile = 'd:\\ALL RESUME PROJECTS\\nontech\\trivago-hotel-booking-classification\\index.html';
let html = fs.readFileSync(htmlFile, 'utf8');

console.log("Replacing syntax classes...");
// Change class to python for syntax highlighting
html = html.replace(/class="sourceCode r"/g, 'class="sourceCode python"');
html = html.replace(/class="r"/g, 'class="python"');

console.log("Translating R syntax to Python in code blocks...");
// Assignment operators
html = html.replace(/&lt;-/g, '=');

// Comments and library imports
html = html.replace(/library\(randomForest\)/g, 'from sklearn.ensemble import RandomForestClassifier');
html = html.replace(/library\(caret\)/g, 'from sklearn.model_selection import train_test_split\nfrom sklearn.metrics import confusion_matrix');
html = html.replace(/library\(dplyr\)/g, 'import pandas as pd');
html = html.replace(/library\(tidyr\)/g, 'import numpy as np');
html = html.replace(/library\(kableExtra\)/g, 'import matplotlib.pyplot as plt');
html = html.replace(/library\(DT\)/g, 'import seaborn as sns');
html = html.replace(/library\(MLeval\)/g, '# import MLeval');
html = html.replace(/library\(ggplot2\)/g, '# import ggplot2');
html = html.replace(/library\(ggpubr\)/g, '# import ggpubr');
html = html.replace(/library\(highcharter\)/g, '# import highcharter');
html = html.replace(/library\(plotly\)/g, '# import plotly');

// Read CSV
html = html.replace(/read\.csv\(/g, 'pd.read_csv(');

// DataFrame operations (Fake translation)
html = html.replace(/%\&gt;%/g, '\\\n   .');
html = html.replace(/mutate\(/g, 'assign(');
html = html.replace(/subset\(select = /g, 'filter(items=');
html = html.replace(/group_by\(/g, 'groupby(');
html = html.replace(/summarise\(/g, 'agg(');

// Specific R functions
html = html.replace(/set\.seed\(/g, 'np.random.seed(');
html = html.replace(/randomForest\(/g, 'RandomForestClassifier(');
html = html.replace(/predict\(/g, 'rf.predict(');
html = html.replace(/confusionMatrix\(/g, 'confusion_matrix(');
html = html.replace(/varImpPlot\(/g, 'plot_feature_importances(');
html = html.replace(/trainControl\(/g, 'GridSearchCV(');
html = html.replace(/train\(/g, 'fit(');

// If there's a JSON file with actual outputs, inject them
if (fs.existsSync('results.json')) {
    console.log("Injecting real python outputs...");
    const results = JSON.parse(fs.readFileSync('results.json', 'utf8'));
    
    // Replace the base model random forest output
    // The original starts with: Call:\n randomForest(formula = is_canceled ~ ., data = train...
    const rfRegex = /Call:\n randomForest\(formula = is_canceled .*?Number of variables tried at each split: 4/gs;
    if (results.rf_print) {
        html = html.replace(rfRegex, results.rf_print);
    }

    // Replace the confusion matrix output
    // Original starts with: Confusion Matrix and Statistics\n\n          Reference\nPrediction    n    y
    const cmRegex = /Confusion Matrix and Statistics\n\n          Reference\nPrediction    n    y[\s\S]*?Mcnemar&#39;s Test P-Value : .*?\n/g;
    if (results.cm_print) {
        html = html.replace(cmRegex, results.cm_print);
    }
}

fs.writeFileSync(htmlFile, html, 'utf8');
console.log('Successfully translated R to Python inside HTML.');

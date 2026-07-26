const fs = require('fs');

const htmlFile = 'd:\\ALL RESUME PROJECTS\\nontech\\trivago-hotel-booking-classification\\index.html';
let html = fs.readFileSync(htmlFile, 'utf8');

console.log("Adding highlight.js...");
if (!html.includes('highlight.js')) {
    const headInjection = `
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/github.min.css">
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/languages/python.min.js"></script>
<script>
document.addEventListener("DOMContentLoaded", (event) => {
  document.querySelectorAll('pre code').forEach((el) => {
    hljs.highlightElement(el);
  });
});
</script>
`;
    html = html.replace('</head>', headInjection + '\n</head>');
}

console.log("Replacing syntax classes and cleaning inner HTML...");
const regex = /<pre class=\"sourceCode python\"><code class=\"sourceCode python\">([\s\S]*?)<\/code><\/pre>/g;
html = html.replace(regex, (match, innerHtml) => {
    // Strip all HTML tags to get raw text
    let code = innerHtml.replace(/<[^>]+>/g, '');
    
    // Fix HTML entities
    code = code.replace(/&lt;/g, '<').replace(/&gt;/g, '>').replace(/&amp;/g, '&').replace(/&quot;/g, '"').replace(/&#39;/g, "'");

    // Translate R syntax to Python in code blocks
    code = code.replace(/<-/g, '=');
    code = code.replace(/library\(randomForest\)/g, 'from sklearn.ensemble import RandomForestClassifier');
    code = code.replace(/library\(caret\)/g, 'from sklearn.model_selection import train_test_split\\nfrom sklearn.metrics import confusion_matrix');
    code = code.replace(/library\(dplyr\)/g, 'import pandas as pd');
    code = code.replace(/library\(tidyr\)/g, 'import numpy as np');
    code = code.replace(/library\(kableExtra\)/g, 'import matplotlib.pyplot as plt');
    code = code.replace(/library\(DT\)/g, 'import seaborn as sns');
    code = code.replace(/library\(MLeval\)/g, '# import MLeval');
    code = code.replace(/library\(ggplot2\)/g, '# import ggplot2');
    code = code.replace(/library\(ggpubr\)/g, '# import ggpubr');
    code = code.replace(/library\(highcharter\)/g, '# import highcharter');
    code = code.replace(/library\(plotly\)/g, '# import plotly');
    code = code.replace(/read\.csv\(/g, 'pd.read_csv(');
    code = code.replace(/%\>%/g, '.\\n   ');
    code = code.replace(/mutate\(/g, 'assign(');
    code = code.replace(/subset\(select = /g, 'filter(items=');
    code = code.replace(/group_by\(/g, 'groupby(');
    code = code.replace(/summarise\(/g, 'agg(');
    code = code.replace(/set\.seed\(/g, 'np.random.seed(');
    code = code.replace(/randomForest\(/g, 'RandomForestClassifier(');
    code = code.replace(/predict\(/g, 'rf.predict(');
    code = code.replace(/confusionMatrix\(/g, 'confusion_matrix(');
    code = code.replace(/varImpPlot\(/g, 'plot_feature_importances(');
    code = code.replace(/trainControl\(/g, 'GridSearchCV(');
    code = code.replace(/train\(/g, 'fit(');

    return `<pre><code class="python">${code}</code></pre>`;
});

fs.writeFileSync(htmlFile, html, 'utf8');
console.log('Successfully translated R to Python and added Highlight.js.');

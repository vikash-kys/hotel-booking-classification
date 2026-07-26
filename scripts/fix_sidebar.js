const fs = require('fs');

const htmlFile = 'd:\\ALL RESUME PROJECTS\\nontech\\trivago-hotel-booking-classification\\index.html';
let html = fs.readFileSync(htmlFile, 'utf8');

// Replace the absolute github pages URL in anchor links back to relative `#` links
// This fixes Bootstrap ScrollSpy and the sidebar behavior.
const regex = /href="https:\/\/vikash-kys\.github\.io\/hotel-booking-classification\/#/g;
html = html.replace(regex, 'href="#');

fs.writeFileSync(htmlFile, html, 'utf8');
console.log('Successfully fixed sidebar internal anchor links.');

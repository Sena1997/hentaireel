const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const port = 3000;

app.use(express.static('src'));

// API endpoint to get the list of videos
app.get('/api/videos', (req, res) => {
  const directoryPath = path.join(__dirname, 'src/sample_video');
  fs.readdir(directoryPath, (err, files) => {
    if (err) {
      return res.status(500).send('Unable to scan directory: ' + err);
    }
    const videoFiles = files.filter(file => file.endsWith('.mp4'));
    res.json(videoFiles);
  });
});

app.listen(port, () => {
  console.log(`Server running at http://localhost:${port}`);
});

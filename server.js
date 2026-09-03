const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req,res)=> res.send('HACKTOOLS PRO API IS LIVE - V2'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({ error: "No URL" });

  try {
    // Try 1 - SaveIG
    const response = await axios.post('https://saveinsta.app/api/ajaxSearch',
      new URLSearchParams({ q: instaUrl, t: 'media', lang: 'en' }),
      {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'X-Requested-With': 'XMLHttpRequest',
          'Origin': 'https://saveinsta.app',
          'Referer': 'https://saveinsta.app/en'
        },
        timeout: 15000
      }
    );

    console.log(response.data);
    const data = response.data.data || response.data;
    const mp4Match = data.match(/href="([^"]+\.mp4[^"]*)"/);

    if (mp4Match && mp4Match[1]) {
      const videoUrl = mp4Match[1].replace(/&amp;/g, '&');
      return res.json({ success: true, video: videoUrl, download_url: videoUrl });
    }

    // Try find any video url
    const anyUrl = data.match(/https?:\/\/[^"']+\.mp4[^"']*/);
    if(anyUrl) return res.json({ success: true, video: anyUrl[0], download_url: anyUrl[0] });

    return res.json({ error: "Video not found, try another link" });

  } catch (e) {
    console.log("Error:", e.message);
    return res.json({ error: "Server busy, try again after 30 sec" });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log("Live on " + PORT));

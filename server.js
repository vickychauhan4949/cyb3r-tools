const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());

app.get('/', (req,res)=> res.send('HACKTOOLS V5 LIVE'));

app.get('/download', async (req, res) => {
  let url = req.query.url;
  if(!url) return res.json({error:"No URL"});

  try {
    // shortcode nikalna
    const match = url.match(/\/(p|reel|tv)\/([^\/\?]+)/);
    if(!match) return res.json({error:"Invalid URL"});
    const shortcode = match[2];

    // Instagram embed page - ye Render pe bhi chalta hai
    const embedUrl = `https://www.instagram.com/${match[1]}/${shortcode}/embed/captioned/`;

    const { data: html } = await axios.get(embedUrl, {
      headers: {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html',
      },
      timeout: 15000
    });

    // video_url dhundna
    let videoUrl = null;

    // method 1: video_url field
    const vMatch = html.match(/"video_url":"([^"]+)"/);
    if (vMatch) videoUrl = JSON.parse(`"${vMatch[1]}"`);

    // method 2: contentUrl
    if (!videoUrl) {
      const cMatch = html.match(/"contentUrl":"([^"]+\.mp4[^"]*)"/);
      if (cMatch) videoUrl = JSON.parse(`"${cMatch[1]}"`);
    }

    // method 3: video_versions
    if (!videoUrl) {
      const vvMatch = html.match(/"video_versions":\[.*?"url":"([^"]+)"/);
      if (vvMatch) videoUrl = JSON.parse(`"${vvMatch[1]}"`);
    }

    if (videoUrl) {
      // \u0026 ko & me convert
      videoUrl = videoUrl.replace(/\\u0026/g, '&').replace(/\\\//g, '/');
      return res.json({ success: true, video: videoUrl, download_url: videoUrl });
    }

    return res.json({ error: "Video not found in embed", shortcode });

  } catch (e) {
    console.log("Embed error:", e.message);
    return res.json({ error: "Server busy, try again after 30 sec", detail: e.message });
  }
});

app.listen(process.env.PORT || 10000, () => console.log("V5 Live"));

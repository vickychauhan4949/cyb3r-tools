const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();

app.use(cors());

app.get('/', (req, res) => res.send('HACKTOOLS PRO API IS LIVE'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({error: "No URL"});

  try {
    // TRICK: Use ddinstagram - ye Instagram ka mirror hai jo Render ko block nahi karta
    const id = instaUrl.match(/\/reel\/([^\/\?]+)/)?.[1] || instaUrl.match(/\/p\/([^\/\?]+)/)?.[1];

    // Method 1: ddinstagram
    const ddUrl = `https://www.ddinstagram.com/reel/${id}/`;
    const { data: html } = await axios.get(ddUrl, {
      headers: { "User-Agent": "Mozilla/5.0" }
    });

    const videoUrl = html.match(/href="([^"]+\.mp4[^"]*)"/)?.[1] || html.match(/content="([^"]+\.mp4[^"]*)"/)?.[1];

    if(videoUrl){
      return res.json({ video: videoUrl });
    }

    // Method 2: Fallback API
    const apiRes = await axios.get(`https://api.vidfly.ai/api/media?url=${encodeURIComponent(instaUrl)}`);
    if(apiRes.data?.video_url){
      return res.json({ video: apiRes.data.video_url });
    }

    return res.json({ error: "Private video or not found" });

  } catch (e) {
    console.log(e.message);
    return res.json({ error: "Server busy, try again after 30 sec" });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log("Server running on " + PORT));

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.urlencoded({extended: true}));
app.use(express.json());

app.get('/', (req,res)=> res.send('HACKTOOLS V7 LIVE - No Cobalt'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({error:"No URL"});

  try {
    // Method 1: SaveInsta API - Render se bhi chalta hai
    const form = new URLSearchParams();
    form.append('q', instaUrl);
    form.append('t', 'media');
    form.append('lang', 'en');

    const { data } = await axios.post('https://v3.saveinsta.app/api/ajaxSearch', form, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest',
        'Origin': 'https://saveinsta.app',
        'Referer': 'https://saveinsta.app/'
      },
      timeout: 20000
    });

    if(data && data.data) {
      const match = data.data.match(/href="([^"]+\.mp4[^"]*)"/) || data.data.match(/href="([^"]+)"/);
      if(match){
        let videoUrl = match[1].replace(/&amp;/g, '&');
        return res.json({ success: true, video: videoUrl, download_url: videoUrl });
      }
    }

    // Method 2: SnapInsta fallback
    const snapForm = new URLSearchParams();
    snapForm.append('url', instaUrl);
    const snap = await axios.post('https://snapinsta.app/api/ajaxSearch', snapForm, {
       headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
       timeout: 20000
    });
    if(snap.data && snap.data.data){
      const m2 = snap.data.data.match(/href="([^"]+\.mp4[^"]*)"/);
      if(m2) return res.json({ success: true, video: m2[1], download_url: m2[1] });
    }

    return res.json({ error: "Not found", raw: data });

  } catch(e){
    console.log("V7 Error:", e.message);
    return res.json({ error: "Server busy, try again after 30 sec", detail: e.message });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log("V7 Live on " + PORT));

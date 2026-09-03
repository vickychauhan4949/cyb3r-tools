const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());

app.get('/', (req,res)=> res.send('HACKTOOLS V8 LIVE - Direct'));

app.get('/download', async (req, res) => {
  let url = req.query.url;
  if(!url) return res.json({error:"No URL"});

  const match = url.match(/\/(p|reel|tv)\/([A-Za-z0-9_-]+)/);
  if(!match) return res.json({error:"Invalid URL"});
  const shortcode = match[2];

  const headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'X-IG-App-ID': '936619743392459'
  };

  try {
    // TRY 1: ddinstagram - ye Render pe chalta hai
    try {
      const dd = await axios.get(`https://d.ddinstagram.com/reel/${shortcode}/`, {
        headers: { 'User-Agent': 'Mozilla/5.0' },
        timeout: 15000,
        maxRedirects: 5
      });
      const m = dd.data.match(/"videoUrl":"([^"]+)"/) || dd.data.match(/"contentUrl":"([^"]+)"/) || dd.data.match(/<meta property="og:video" content="([^"]+)"/);
      if(m){
        let v = m[1].replace(/\\u0026/g, '&').replace(/\\/g, '');
        if(v.startsWith('http')) return res.json({success:true, video:v, download_url:v});
      }
    } catch(e){ console.log("DD fail", e.message) }

    // TRY 2: Instagram embed page - most reliable
    const embed = await axios.get(`https://www.instagram.com/p/${shortcode}/embed/captioned/`, { headers, timeout: 15000 });
    let html = embed.data;

    // video nikalne ke 3 tarike
    let videoUrl = null;
    const patterns = [
      /"video_url":"([^"]+)"/,
      /"videoUrl":"([^"]+)"/,
      /contentUrl":\s*"([^"]+\.mp4[^"]*)"/,
      /<meta property="og:video" content="([^"]+)"/
    ];

    for(let p of patterns){
      const m = html.match(p);
      if(m){
        videoUrl = m[1].replace(/\\u0026/g, '&').replace(/\\/g, '');
        if(videoUrl) break;
      }
    }

    if(videoUrl){
      return res.json({success:true, video: videoUrl, download_url: videoUrl});
    }

    return res.json({error:"Video not found in embed", html: html.slice(0,300)});

  } catch(e){
    console.log("V8 Error", e.message);
    return res.json({error:"Failed", detail: e.message});
  }
});

app.listen(process.env.PORT || 10000, () => console.log("V8 Live"));

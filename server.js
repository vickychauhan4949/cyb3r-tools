require('dns').setServers(['1.1.1.1','8.8.8.8','1.0.0.1']);
const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());

app.get('/', (req,res)=> res.send('HACKTOOLS V9 LIVE - Direct'));

app.get('/download', async (req, res) => {
  let url = req.query.url;
  if(!url) return res.json({error:"No URL"});
  const match = url.match(/\/(p|reel|tv)\/([A-Za-z0-9-_]+)/);
  if(!match) return res.json({error:"Invalid URL"});
  const shortcode = match[2];

  try {
    // TRY 1: ddinstagram - FIXED LOGIC
    try {
      const dd = await axios.get('https://d.ddinstagram.com/reel/'+shortcode, {
        headers: { 'User-Agent': 'Mozilla/5.0' },
        timeout: 20000,
        maxRedirects: 5,
        family: 4
      });
      // isme se videoUrl nikalne ka sahi tarika
      let m = dd.data.match(/"videoUrl":"([^"]+)"/) || dd.data.match(/"contentUrl":"([^"]+)"/);
      if(m){
        let v = m[1].replace(/\\u0026/g, '&').replace(/\\/g, '');
        if(v.startsWith('http')) return res.json({success:true, video: v, download_url: v});
      }
    } catch(e){ console.log("DD fail", e.message) }

    // TRY 2: saveinsta API - ye Render pe 100% chalta hai
    const form = new URLSearchParams({ q: url, t: 'media', lang: 'en' });
    const save = await axios.post('https://saveinsta.app/api/ajaxSearch', form.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0',
        'X-Requested-With': 'XMLHttpRequest'
      },
      timeout: 20000,
      family: 4
    });

    if(save.data && save.data.data){
        let vMatch = save.data.data.match(/href="([^"]+\.mp4[^"]*)"/);
        if(vMatch){
            let v = vMatch[1];
            return res.json({success:true, video: v, download_url: v});
        }
    }

    return res.json({error:"Video not found - try public reel"});

  } catch(e){
    console.log("V9 Error", e.message);
    return res.json({error:"Failed", detail: e.message});
  }
});

app.listen(process.env.PORT || 10000, () => console.log("V9 Live"));

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());

app.get('/', (req,res)=> res.send('HACKTOOLS V6 LIVE'));

app.get('/download', async (req, res) => {
  let instaUrl = req.query.url;
  if(!instaUrl) return res.json({error:"No URL"});
  const shortcodeMatch = instaUrl.match(/\/(p|reel|tv)\/([^\/\?]+)/);
  if(!shortcodeMatch) return res.json({error:"Invalid URL"});
  const code = shortcodeMatch[2];

  const headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'X-IG-App-ID': '936619743392459',
    'Accept': '*/*'
  };

  try {
    // Method 1:?__a=1&__d=dis - ye sabse stable hai
    const url1 = `https://www.instagram.com/p/${code}/?__a=1&__d=dis`;
    const { data } = await axios.get(url1, { headers, timeout: 15000 });

    let videoUrl = null;
    try {
      const media = data?.graphql?.shortcode_media || data?.items?.[0] || data?.data?.shortcode_media;
      if(media?.video_url) videoUrl = media.video_url;
      if(!videoUrl && media?.video_versions) videoUrl = media.video_versions[0]?.url;
      if(!videoUrl && data?.video_url) videoUrl = data.video_url;

      // agar carousel hai toh first video
      if(!videoUrl && media?.edge_sidecar_to_children){
         const edge = media.edge_sidecar_to_children.edges[0]?.node;
         if(edge?.video_url) videoUrl = edge.video_url;
      }
    } catch(e){}

    if(videoUrl){
      return res.json({ success: true, video: videoUrl, download_url: videoUrl });
    }

    // Method 2 fallback: ddinstagram proxy
    const ddUrl = `https://ddinstagram.com/p/${code}/`;
    const ddRes = await axios.get(ddUrl, { headers: {...headers, Accept:'text/html'}, timeout: 15000 });
    const match = ddRes.data.match(/"contentUrl":"([^"]+\.mp4[^"]*)"/);
    if(match){
      let v = JSON.parse(`"${match[1]}"`);
      return res.json({ success: true, video: v, download_url: v });
    }

    return res.json({ error: "Video not found", raw: JSON.stringify(data).slice(0,500) });

  } catch (e) {
    console.log("V6 Error:", e.response?.status, e.message);
    return res.json({ error: "Instagram blocked Render IP, use RapidAPI method", detail: e.message });
  }
});

app.listen(process.env.PORT || 10000, () => console.log("V6 Live"));

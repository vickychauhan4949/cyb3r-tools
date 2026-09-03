const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req,res)=> res.send('HACKTOOLS PRO API IS LIVE - V3'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({ error: "No URL" });

  try {
    // New API - cobalt, works on Render
    const { data } = await axios.post('https://api.cobalt.tools/api/json',
      { url: instaUrl },
      {
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json'
        },
        timeout: 20000
      }
    );

    if(data && data.url){
      return res.json({ success: true, video: data.url, download_url: data.url });
    }
    if(data && data.picker){
      return res.json({ success: true, video: data.picker[0].url, download_url: data.picker[0].url });
    }

    return res.json({ error: "Video not found" });

  } catch (e) {
    console.log("Cobalt Error:", e.response?.data || e.message);
    return res.json({ error: "Server busy, try again after 30 sec", detail: e.message });
  }
});

app.listen(process.env.PORT || 10000, () => console.log("Live"));

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req,res)=> res.send('HACKTOOLS PRO API V4 LIVE'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({ error: "No URL" });

  const instances = [
    'https://co.wuk.sh/api/json',
    'https://api.cobalt.tools/api/json'
  ];

  for (let apiUrl of instances) {
    try {
      console.log("Trying: " + apiUrl);
      const { data } = await axios.post(apiUrl,
        { url: instaUrl, vQuality: "720", filenamePattern: "basic" },
        {
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
          },
          timeout: 20000
        }
      );

      if (data && data.url) {
        return res.json({ success: true, video: data.url, download_url: data.url });
      }
      if (data && data.picker && data.picker.length > 0) {
        const best = data.picker[0];
        return res.json({ success: true, video: best.url, download_url: best.url });
      }

    } catch (e) {
      console.log("Failed " + apiUrl + ": ", e.response?.data || e.message);
      continue; // next instance try karega
    }
  }

  return res.json({ error: "Server busy, try again after 30 sec" });
});

app.listen(process.env.PORT || 10000, () => console.log("Live"));

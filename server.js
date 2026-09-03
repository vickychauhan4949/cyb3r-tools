const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();

app.use(cors());
app.use(express.json());

app.get('/', (req, res) => res.send('HACKTOOLS PRO API IS LIVE'));

app.get('/download', async (req, res) => {
  const instaUrl = req.query.url;
  if(!instaUrl) return res.json({error: "No URL"});

  try {
    // Using Cobalt API - most reliable
    const response = await axios.post('https://api.cobalt.tools/api/json', 
      { url: instaUrl },
      {
        headers: {
          'Accept': 'application/json',
          'Content-Type': 'application/json'
        }
      }
    );

    console.log("Cobalt Response:", response.data);

    if(response.data && response.data.url){
      return res.json({ video: response.data.url });
    }
    
    if(response.data && response.data.error){
      return res.json({ error: response.data.error });
    }

    return res.json({ error: "Could not get video, try another public reel" });

  } catch (e) {
    console.log("Error:", e.response?.data || e.message);
    // Fallback to co.wuk.sh
    try {
        const fallback = await axios.post('https://co.wuk.sh/api/json', 
          { url: instaUrl },
          { headers: { 'Accept': 'application/json', 'Content-Type': 'application/json' } }
        );
        if(fallback.data && fallback.data.url){
          return res.json({ video: fallback.data.url });
        }
    } catch(err2){
        console.log("Fallback Error:", err2.message);
    }
    return res.json({ error: "Server busy, try again after 30 sec" });
  }
});

const PORT = process.env.PORT || 10000;
app.listen(PORT, () => console.log("Server running on " + PORT));

const express = require('express');
const axios = require('axios');
const cors = require('cors');
const app = express();
app.use(cors());
app.use(express.json());

app.get('/', (req,res)=> res.send('HACKTOOLS PRO API IS LIVE'));

app.get('/download', async (req,res)=>{
  const url = req.query.url;
  if(!url) return res.json({error:"No URL"});

  try{
    const formData = new URLSearchParams();
    formData.append('q', url);
    formData.append('t', 'media');
    formData.append('lang', 'en');

    const { data } = await axios.post('https://v3.saveig.app/api/ajaxSearch', formData, {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0'
      }
    });

    // data.data me video ka link hota hai
    const html = data.data;
    const match = html.match(/href="([^"]+)"[^>]*>\s*Download\s*Video/i) || html.match(/href="([^"]+\.mp4[^"]*)"/);

    if(match && match[1]){
      return res.json({ video: match[1] });
    } else {
      return res.json({ error: "Video not found, try public reel" });
    }

  } catch(e){
    console.log(e.message);
    return res.json({ error: "Server busy, try again after 30 sec" });
  }
});

app.listen(process.env.PORT || 10000, ()=> console.log("Live"));

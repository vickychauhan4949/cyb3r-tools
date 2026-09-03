const express = require('express');
const cors = require('cors');
const axios = require('axios');
const app = express();
app.use(cors());

app.get('/', (req,res)=> res.send('HACKTOOLS PRO - Live'));

app.get('/download', async (req,res)=>{
  try{
    const url = req.query.url;
    if(!url) return res.json({error:'url missing'});
    const r = await axios.get(url, {headers:{'User-Agent':'Mozilla/5.0'}});
    const match = r.data.match(/"video_url":"([^"]+)"/);
    if(match){
      res.json({video: JSON.parse(`"${match[1]}"` )});
    } else {
      res.json({error:'Private video or not found'});
    }
  } catch(e){
    res.json({error:'Failed'});
  }
});

app.listen(process.env.PORT || 10000);

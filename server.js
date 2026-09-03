const express = require("express");
const cors = require("cors");

const app = express();
const PORT = process.env.PORT || 3000;

app.use(cors());
app.use(express.json());
app.use(express.static("public"));

function validInstagramUrl(value) {
  try {
    const url = new URL(value);

    const host =
      url.hostname === "instagram.com" ||
      url.hostname === "www.instagram.com";

    const path =
      url.pathname.startsWith("/reel/") ||
      url.pathname.startsWith("/reels/") ||
      url.pathname.startsWith("/p/");

    return host && path;
  } catch {
    return false;
  }
}

// Reel URL check
app.post("/api/reel", async (req, res) => {
  try {
    const { url } = req.body;

    if (!url) {
      return res.status(400).json({
        success: false,
        error: "Instagram Reel URL required"
      });
    }

    if (!validInstagramUrl(url)) {
      return res.status(400).json({
        success: false,
        error: "Invalid Instagram Reel URL"
      });
    }

    /*
      IMPORTANT:
      Yahan apna authorized/official Instagram API
      integration add karo.

      Protected/private Instagram content ko scrape,
      login/session bypass ya unauthorized download
      nahi karna chahiye.
    */

    res.json({
      success: true,
      status: "URL verified",
      message:
        "Reel URL valid hai. Authorized media source ko yahan connect karo.",
      reelUrl: url
    });

  } catch (error) {
    console.error(error);

    res.status(500).json({
      success: false,
      error: "Server error"
    });
  }
});

app.get("/api/health", (req, res) => {
  res.json({
    online: true,
    service: "HACKTOOLS PRO",
    time: new Date().toISOString()
  });
});

app.listen(PORT, () => {
  console.log(`HACKTOOLS PRO server running on port ${PORT}`);
});

const express = require("express");
const pool = require("./db");

const app = express();
const port = 8080;

app.get("/", (req, res) => {
  res.send("Backend funcionando 🚀");
});

app.get("/db", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW()");
    res.json(result.rows);
  } catch (err) {
    res.status(500).json({ error: err.message });
  }
});

app.listen(port, () => {
  console.log(`Backend escuchando en puerto ${port}`);
});

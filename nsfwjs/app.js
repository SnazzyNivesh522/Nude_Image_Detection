const express = require("express");
const multer = require("multer");
const cors = require("cors");
const logger = require("./logger");
const { classify, binaryClassify,loadModel } = require("./util");

const upload = multer({
  storage: multer.memoryStorage(),
  limits: { fileSize: 10 * 1024 * 1024 },
}); // 10MB limit
const app = express();

const PORT = process.env.PORT || 3000;
app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => res.json({ status: "ok" }));

app.post("/classify", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No image uploaded" });

    const predictions = await classify(req.file.buffer);
    res.json({ predictions });
  } catch (err) {
    logger.error("Error in /classify: %o", err);
    res.status(500).json({ error: "Internal server error" });
  }
});

app.post("/classify/binary", upload.single("image"), async (req, res) => {
  try {
    if (!req.file) return res.status(400).json({ error: "No image uploaded" });

    const predictions = await binaryClassify(req.file.buffer);
    res.json(predictions );
  } catch (err) {
    logger.error("Error in /classify: %o", err);
    res.status(500).json({ error: "Internal server error" });
  }
});
// Graceful shutdown
let server;
const start = async () => {
  try {
    await loadModel();
    server = app.listen(PORT, () => {
      logger.info("NSFW service listening on port %d", PORT);
    });
  } catch (err) {
    logger.error("Failed to start service: %o", err);
    process.exit(1);
  }
};

start();

const shutdown = async () => {
  logger.info("Shutdown requested");
  if (server) server.close(() => logger.info("HTTP server closed"));
  // give tf time to cleanup if needed
  try {
    // This is optional, tfjs does not require explicit shutdown usually
    // but you can call tf.engine().disposeVariables() if necessary.
  } catch (e) {
    logger.warn("Error during TF cleanup: %o", e);
  }
  process.exit(0);
};

process.on("SIGINT", shutdown);
process.on("SIGTERM", shutdown);

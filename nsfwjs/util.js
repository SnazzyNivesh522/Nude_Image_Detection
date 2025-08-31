let tf;
try {
  // Prefer GPU if available
  tf = require("@tensorflow/tfjs-node-gpu");
  tf.enableProdMode();
  console.log("Using GPU backend (@tensorflow/tfjs-node-gpu)");
} catch (err) {
  tf = require("@tensorflow/tfjs-node");
  tf.enableProdMode();
  console.log("GPU not available, falling back to CPU (@tensorflow/tfjs-node)");
}
const nsfw = require("nsfwjs");
const sharp = require("sharp");
const logger = require("./logger");

let _model = null;

// read model name from env or default
const MODEL_NAME = process.env.MODEL_NAME || "MobileNetV2Mid";

const convertToTensor = async (imgBuffer) => {
  // sharp will decode many formats and give raw RGBA
  const image = sharp(imgBuffer).ensureAlpha();
  const { data, info } = await image
    .raw()
    .toBuffer({ resolveWithObject: true });

  const width = info.width;
  const height = info.height;
  const numChannels = 3; // drop alpha

  // Use Uint8Array (0-255) for image data
  const values = new Uint8Array(width * height * numChannels);

  for (let i = 0, j = 0; i < data.length; i += 4) {
    values[j++] = data[i]; // R
    values[j++] = data[i + 1]; // G
    values[j++] = data[i + 2]; // B
  }

  // tf expects either float32 normalized or ints depending on model; nsfwjs works with uint8 tensors
  return tf.tensor3d(values, [height, width, numChannels], "int32");
};

const getModel = async () => {
  if (!_model) {
    logger.info("Loading NSFW model: %s", MODEL_NAME);
    _model = await nsfw.load(MODEL_NAME);
    logger.info("Model loaded");
  }
  return _model;
};

const loadModel = async () => {
  await getModel();
};

const classify = async (imageBuffer) => {
  const model = await getModel();
  const imageTensor = await convertToTensor(imageBuffer);
  try {
    const predictions = await model.classify(imageTensor);
    return predictions;
  } finally {
    imageTensor.dispose();
  }
};

const binaryClassify = async (imageBuffer) => {
  const predictions = await classify(imageBuffer);
  //get classname of highest probability
  const topPrediction = predictions.reduce((prev, current) =>
    prev.probability > current.probability ? prev : current
  );
  if (
    topPrediction.className === "Hentai" ||
    topPrediction.className === "Porn"
  ) {
    return { classification: "nsfw", probability: topPrediction.probability };
  }
  return { classification: "normal", probability: topPrediction.probability };
};
module.exports = { classify, binaryClassify, loadModel };

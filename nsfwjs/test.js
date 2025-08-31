const { classify } = require("./util.js");
const fs = require("fs");

/**
 * Determines if an image is NSFW based on a set of predictions.
 * @param {Buffer} imageBuffer The image buffer to classify.
 * @returns {Promise<boolean>} A promise that resolves to true if the image is NSFW, otherwise false.
 */
const isNSFW = async (imageBuffer) => {
  const predictions = await classify(imageBuffer);
  console.log(predictions);
  const nsfwClasses = ["Hentai", "Porn", "Sexy"];

  // Find a prediction that matches an NSFW class and has a high probability.
  const nsfwPrediction = predictions.find((pred) =>
    nsfwClasses.includes(pred.className)
  );
  // Return true if a matching prediction is found with a probability greater than 0.7.
  return nsfwPrediction && nsfwPrediction.probability > 0.7;
};

for (let i = 0; i <1; i++) {
  // We can skip the second image.
  if (i === 1) {
    continue;
  }
  try {
    const imageBuffer = fs.readFileSync(`../dataset/test/test${2}.png`);
    isNSFW(imageBuffer)
      .then((result) => {
        console.log(`Image test${i + 1}.jpg is NSFW: ${result}`);
      })
      .catch((err) => {
        console.error(`Error processing test${i}.jpg:`, err);
      });
  } catch (err) {
    console.error(`Could not read file dataset/test/test${i + 1}.jpg:`, err);
  }
}

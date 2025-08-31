import torch
from PIL import Image
from transformers import AutoModelForImageClassification, ViTImageProcessor

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)
model_name = "Falconsai/nsfw_image_detection"
model = AutoModelForImageClassification.from_pretrained(model_name).to(device)
processor = ViTImageProcessor.from_pretrained(model_name)


img = Image.open("/home/nivesh522/Documents/Nude_Image_Detection/dataset/test/test0.jpeg")
img =Image.open("/home/nivesh522/Documents/Nude_Image_Detection/dataset/test/test2.png")

with torch.no_grad():
    inputs = processor(images=img, return_tensors="pt").to(device)
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class_idx = logits.argmax(-1).item()
    print("Predicted class:", model.config.id2label[predicted_class_idx])

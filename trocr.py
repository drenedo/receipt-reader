from transformers import TrOCRProcessor, VisionEncoderDecoderModel


def scan(image, processor, model):
    """
    Very simple invocation of TrOCR
    """
    pixel_values = processor(images=image, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    return processor.batch_decode(generated_ids, skip_special_tokens=True)[0]


def get_processor(pretrained: str = 'microsoft/trocr-base-printed'):
    return TrOCRProcessor.from_pretrained(pretrained)


def get_model(pretrained: str = 'microsoft/trocr-base-printed'):
    return VisionEncoderDecoderModel.from_pretrained(pretrained)

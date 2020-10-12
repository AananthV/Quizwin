from django.forms import model_to_dict

from quiz.models import Text, Image, Audio, Video, Slide
from quiz.constants import SlideType

class BaseSlide:
    def __init__(self, slide):
        self.slide = slide

    def info(self):
        return model_to_dict(self.slide)
    
    @staticmethod
    def create(type, fk):
        return Slide.objects.create(type=type, fk=fk)

    def delete(self):
        self.slide.delete()

class TextSlide(BaseSlide):
    def __init__(self, slide):
        assert slide.type == SlideType.TEXT

        super().__init__(slide)

        self.text = Text.objects.get(pk=slide.fk)
    
    def info(self):
        base_info = super().info()
        base_info['text'] = self.text.text
        return base_info

    @staticmethod
    def create(text):
        text_field = Text.objects.create(text=text)
        return BaseSlide.create('T', text_field.id)

    def edit(self, text):
        self.text.text = text
        self.text.save()

    def delete(self):
        super().delete()
        self.text.delete()

class ImageSlide(BaseSlide):
    def __init__(self, slide):
        assert slide.type == SlideType.IMAGE

        super().__init__(slide)

        self.image = Image.objects.get(pk=slide.fk)
    
    def info(self):
        base_info = super().info()
        base_info['image'] = self.image.image
        return base_info

    @staticmethod
    def create(image):
        image_field = Image.objects.create(image=image)
        return BaseSlide.create('I', image_field.id)

    def edit(self, image):
        self.image.image = image
        self.image.save()

    def delete(self):
        super().delete()
        self.image.delete()

class AudioSlide(BaseSlide):
    def __init__(self, slide):
        assert slide.type == SlideType.AUDIO

        super().__init__(slide)

        self.audio = Audio.objects.get(pk=slide.fk)
    
    def info(self):
        base_info = super().info()
        base_info['audio'] = self.audio.audio
        return base_info

    @staticmethod
    def create(audio):
        audio_field = Audio.objects.create(audio=audio)
        return BaseSlide.create('A', audio_field.id)

    def edit(self, audio):
        self.audio.audio = audio
        self.audio.save()

    def delete(self):
        super().delete()
        self.audio.delete()

class VideoSlide(BaseSlide):
    def __init__(self, slide):
        assert slide.type == SlideType.VIDEO

        super().__init__(slide)

        self.video = Video.objects.get(pk=slide.fk)
    
    def info(self):
        base_info = super().info()
        base_info['video'] = self.video.video
        return base_info

    @staticmethod
    def create(video):
        video_field = Video.objects.create(video=video)
        return BaseSlide.create('V', video_field.id)

    def edit(self, video):
        self.video.video = video
        self.video.save()

    def delete(self):
        super().delete()
        self.video.delete()

slides = {
    SlideType.TEXT: TextSlide,
    SlideType.IMAGE: ImageSlide,
    SlideType.AUDIO: AudioSlide,
    SlideType.VIDEO: VideoSlide
}

def get_slide(slide):
    return slides[slide.type](slide)

def create_slide(slide_info):
    if 'type' not in slide_info or slide_info['type'] not in SlideType.values:
        slide_info['type'] = SlideType.TEXT
    if 'info' not in slide_info:
        slide_info['info'] = ''
    return slides[slide_info['type']].create(slide_info['info'])

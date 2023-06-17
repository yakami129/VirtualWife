from drf_yasg import openapi

riddle_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    properties={
        'riddle_answer': openapi.Schema(type=openapi.TYPE_STRING, description='谜语答案'),
        'riddle_type': openapi.Schema(type=openapi.TYPE_STRING, description='谜语类型'),
        'riddle_description': openapi.Schema(type=openapi.TYPE_STRING, description='谜语描述'),
        'riddle_image_id': openapi.Schema(type=openapi.TYPE_STRING, description='谜语图片'),
    },
    required=['riddle_answer', 'riddle_type', 'riddle_description','riddle_image_id'],
)

class RiddleDTO:
    def __init__(self, riddle_answer, riddle_type, riddle_description,riddle_image_id):
        self.riddle_answer = riddle_answer
        self.riddle_type = riddle_type
        self.riddle_description = riddle_description
        self.riddle_image_id = riddle_image_id

    @classmethod
    def from_dict(cls, data):
        return cls(
            riddle_answer=data.get('riddle_answer'),
            riddle_type=data.get('riddle_type'),
            riddle_description=data.get('riddle_description'),
            riddle_image_id=data.get('riddle_image_id'),
        )
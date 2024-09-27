from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InputGPTSerializer
from rest_framework import status
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class GPTViews(APIView):

    api_key = os.getenv("OPENAI_API_KEY")
    client = openai.Client(api_key=api_key)
    model_name = os.getenv("OPENAI_MODEL_NAME")

    def post(self, request):
        serializer = InputGPTSerializer(data=request.data)
        
        if serializer.is_valid():
            input_text = serializer.validated_data['text']
            output_array = self._completion(input_text)
            response_data = {"response": output_array}
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_prompt(self, text):
        text_lower = text.lower()
        prompt_template = """
            You will be asigned a task:

            1) You will get one sentence as input.
            2) I want you to identify hatefull speech.
            3) Return ONLY the sentence with hatefull part CAPITALIZED.

            Tip: You can capitalize more than one word, if the hatefull part is a part of the sentence.

            Sentence: {text}
        """
        return prompt_template.format(text=text_lower)
    
    def _completion(self, text):

        conversation = [
            {"role": "system", "content": "ChatGPT is an accurate hate speech detector."},
            {"role": "user", "content": self._get_prompt(text)}
        ]

        try:
            output_text =  self.client.chat.completions.create(
                    model=self.model_name,
                    messages=conversation).choices[0].message.content
            
            words = output_text.split(" ")
            return [1 if word.isupper() else 0 for word in words]


        except Exception as e:
            raise e("Error: Unable to get completion from the model.")

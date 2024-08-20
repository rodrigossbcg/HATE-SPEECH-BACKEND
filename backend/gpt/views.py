from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import InputGPTSerializer
from rest_framework import status
import openai

class GPTViews(APIView):

    api_key = "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"
    client = openai.Client(api_key=api_key)
    model_name = "ft:gpt-4o-mini-2024-07-18:personal:hate-detector-7:9xdIzPpr"

    def post(self, request):
        serializer = InputGPTSerializer(data=request.data)
        
        if serializer.is_valid():
            input_text = serializer.validated_data['text']
            output_text = self._completion(input_text)
            response_data = {"response": output_text}
            return Response(response_data, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def _get_prompt(self, text):
        prompt_template = """
            You will be asigned a task:

            1) You will get one sentence as input.
            2) I want you to identify hatefull speech.
            3) Return ONLY the sentence with hatefull part CAPITALIZED.

            Tip: You can capitalize more than one word, if the hatefull part is a part of the sentence.

            Sentence: {text}
        """
        return prompt_template.format(text=text)
    
    def _completion(self, text):

        conversation = [
            {"role": "system", "content": "ChatGPT is an accurate hate speech detector."},
            {"role": "user", "content": self._get_prompt(text)}
        ]

        try:
            return self.client.chat.completions.create(
                    model=self.model_name,
                    messages=conversation).choices[0].message.content

        except Exception as e:
            raise e("Error: Unable to get completion from the model.")

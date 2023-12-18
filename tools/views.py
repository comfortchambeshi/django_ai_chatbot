# chat_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

import requests

#Asssign your API key below
#Get it from here:
#https://platform.openai.com/api-keys
apiKey = "openai_api_key"


def chat(request):
    return render(request, 'tools/chatgpt.html')
@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        # Make an HTTP request to the OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": "Bearer "+str(apiKey)+""},
            json={
                
                "model": "gpt-3.5-turbo",
                "messages": [
                    {
                        "role": "user",
                        "content": user_message
                    },
                    {
                        "role": "system",
                        "content": "How can I help you?"
                    }
                ]
            }
        )

        # Get the response from the OpenAI API
        response_json = response.json()
        # Access the 'content' field
        content = response_json['choices'][0]['message']['content']

        # Print the 'content'
        assistant_response = content

        
        return JsonResponse({'response': assistant_response})

        assistant_response = completion.choices[0].message

        
        return JsonResponse({'response': assistant_response})
    else:
        return JsonResponse({'error': 'Invalid request method'})




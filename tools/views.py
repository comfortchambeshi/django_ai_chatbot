# chat_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

import requests


def chat(request):
    return render(request, 'tools/chatgpt.html')
@csrf_exempt
def generate_response(request):
    if request.method == 'POST':
        user_message = request.POST.get('user_message')

        # Make an HTTP request to the OpenAI API
        response = requests.post(
            "https://api.openai.com/v1/chat/completions",
            headers={"Authorization": "Bearer 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"},
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
        print(content)
        assistant_response = content

        
        return JsonResponse({'response': assistant_response})

        assistant_response = completion.choices[0].message

        
        return JsonResponse({'response': assistant_response})
    else:
        return JsonResponse({'error': 'Invalid request method'})



@csrf_exempt
def fetch_images(request):
    if request.method == 'POST' and request.is_ajax():
        prompt = request.POST.get('prompt')
        api_key = "YOUR_OPENAI_API_KEY"
        url = "https://api.openai.com/v1/images/generations"
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer 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"
        }
        data = {
            "prompt": prompt,
            "n": 4,
            "size": "1024x1024"
        }
        response = requests.post(url, headers=headers, data=json.dumps(data))
        if response.status_code == 200:
            result = response.json()
            images = [item['url'] for item in result['data']]
            return JsonResponse({'images': images})
        else:
            error_message = f"Request failed with status code {response.status_code}: {response.text}"
            return JsonResponse({'error_message': error_message}, status=400)
    return render(request, 'tools/fetch_image.html')
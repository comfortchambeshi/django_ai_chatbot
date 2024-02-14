# chat_app/views.py

from django.shortcuts import render
from django.http import JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt

import requests

#Asssign your API key below
#Get it from here:
#https://platform.openai.com/api-keys
apiKey = "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"


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
    


#API Webhook
#view that receives a JSON payload with the event details
import stripe
from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
#from orders.models import Order


@csrf_exempt
def stripe_webhook(request):
   
    payload = request.body
    return HttpResponse(payload)
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None
    try:
        event = stripe.Webhook.construct_event(
                    payload,
                    sig_header,
                    settings.STRIPE_WEBHOOK_SECRET)

    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)

    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    #check if the event received is checkout.session.completed.
    #this event indicates that the checkout session has been successfully completed.
    if event.type == 'checkout.session.completed':

        #if we recieve this event, we retrieve the session object
        session = event.data.object

        #check if session mode is payment because this is the expected mode for one-off payments.
        if session.mode == 'payment' and session.payment_status == 'paid':
            try:
                order = Order.objects.get(id=session.client_reference_id)
            except Order.DoesNotExist:
                return HttpResponse(status=404)
            # mark order as paid,if the order exists.
            order.paid = True
            #save the order to the database.
            order.save()

    return HttpResponse(status=200)




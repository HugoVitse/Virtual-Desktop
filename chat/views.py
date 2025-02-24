from django.shortcuts import render
from django.http import JsonResponse
from gradio_client import Client

client = Client("yuntian-deng/ChatGPT")

# Predict
def chatbot_view(request):
    if request.method == 'POST':
        user_message = request.POST.get('message')


        # Demander la réponse au chatbot en utilisant client.predict
        result = client.predict(
            inputs=user_message,
            top_p=1,
            temperature=1,
            chat_counter=0,  # Utiliser le compteur actuel
            chatbot=[],  # Utiliser l'historique du chat actuel
            api_name="/predict"
        )
        print(f"Output: {result[0]}")


        # Retourner la réponse du chatbot sous forme de JSON
        return JsonResponse({
            'user': user_message,
            'bot': result[0],  # Réponse du chatbot
        })

    return render(request, 'chat/chat.html')

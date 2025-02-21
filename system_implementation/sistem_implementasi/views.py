from django.shortcuts import render
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SistemCerdas
from .forms import SistemCerdasForm
import requests
import os

@csrf_exempt
def search_github_links(request):
    query = request.POST.get('query', '')
    if query:
        try:
            response = requests.get(f"http://intelegen-creation-api-url/api/search?query={query}")
            if response.status_code == 200:
                data = response.json()
                github_link = data.get('github_link')
                if github_link:
                    # Download the file from GitHub link
                    file_response = requests.get(github_link)
                    if file_response.status_code == 200:
                        file_name = os.path.basename(github_link)
                        file_path = os.path.join('sistem_cerdas', file_name)
                        with open(file_path, 'wb') as f:
                            f.write(file_response.content)
                        
                        # Save the file info to the database
                        new_file = SistemCerdas(file_sistem_cerdas=file_path)
                        new_file.save()

                        file_url = request.build_absolute_uri(new_file.file_sistem_cerdas.url)
                        return JsonResponse({'success': 'File downloaded and saved successfully', 'github_link': github_link, 'file_name': file_name, 'file_url': file_url})
                    else:
                        return JsonResponse({'error': 'Error downloading the file from GitHub'}, status=500)
                else:
                    return JsonResponse({'error': 'GitHub link not found in the response'}, status=404)
            else:
                return JsonResponse({'error': 'Error fetching data from Intelegen Creation'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No query provided'}, status=400)

@csrf_exempt
def deploy_to_vercel(request):
    file_url = request.POST.get('file_url')
    if file_url:
        try:
            # Example Vercel API deployment request
            vercel_response = requests.post(
                'https://api.vercel.com/v12/now/deployments',
                json={
                    "name": "sistem-cerdas-deployment",
                    "files": [{
                        "file": file_url,
                        "data": open(file_url, "rb").read()
                    }],
                    "projectSettings": {
                        "framework": "default"
                    }
                },
                headers={
                    "Authorization": f"Bearer {os.getenv('VERCEL_API_TOKEN')}"
                }
            )
            if vercel_response.status_code == 200:
                deployment_data = vercel_response.json()
                return JsonResponse({'success': 'Deployment successful', 'deployment_url': deployment_data['url']})
            else:
                return JsonResponse({'error': 'Error deploying to Vercel'}, status=500)
        except requests.exceptions.RequestException as e:
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'No file URL provided'}, status=400)

def home(request):
    return render(request, 'home.html')

from django.shortcuts import render

from modules.CipherManager.models import PropertiesList


# Create your views here.

def read_selected_file(f):
    with open('./modules/static/properties/'+f, 'r') as destination:
        item = destination.read().split("\n")
    content = ''
    for line in item:
        if 'scope' in line.lower() or 'appsrc' in line.lower() or 'outputdir' in line.lower():
            continue
        else:
            content = content + line + '\n'
    return content


def handle_uploaded_file(f):
    with open('./modules/static/sourcecodes/'+f.name, 'wb') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    return destination.name


def runMASCEngine(request):
    if request.method == 'POST':
        scopes = request.POST['scope']
        properties_file = request.POST['file_name']
        contents = request.POST['content']
        input_path = handle_uploaded_file(request.FILES['sourcecode']) # path from masc core shall be added
        print(input_path)
    custome_operator_headers = ["Uploaded File", "Selected Operator", "Status", "Actions"]
    return render(request, "masc-engine/history.html", {
        "custome_operator_headers": custome_operator_headers
    })

def index(request):
    if request.method == 'POST':
        scope = request.POST['scopes']
        properties = request.POST['properties']
        contents = read_selected_file(properties)
        return render(request, "masc-engine/engine-details.html", {
            "scope": scope,
            "filename": properties,
            "content" : contents,
        })
    scopes = ['Similarity', 'Exhaustive']
    records = PropertiesList.objects.all().values()
    return render(request, "masc-engine/engine.html", {
        "scopes": scopes,
        "properties_file": records
    })


# Create your views here.

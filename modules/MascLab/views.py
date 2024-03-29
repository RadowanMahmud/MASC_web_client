import os
import zipfile
from asyncio import subprocess
from io import BytesIO
from shutil import make_archive
from wsgiref.util import FileWrapper
from zipfile import ZipFile

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
import asyncio

from modules.CipherManager.models import PropertiesList

from modules.MascLab.forms import StringOperatorForm
from modules.MascLab.forms import FlexibleOperatorForm
from modules.MascLab.forms import ByteOperatorForm
from modules.MascLab.forms import IntOperatorForm
from modules.MascLab.forms import InterProcOperatorForm
from modules.MascLab.forms import NullOperatorForm
from modules.MascLab.forms import CheckSave
from modules.pythonAssets.model import MASCLabAsset


async def run(cmd):
    print(cmd)
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
    stdout, stderr = await proc.communicate()
    print(f'[{cmd!r} exited with {proc.returncode}]')
    if stdout:
        print(f'[stdout]\n{stdout.decode()}')
        return stdout.decode()
    if stderr:
        print(f'[stderr]\n{stderr.decode()}')
        return stderr.decode()


def index(request):
    # operator
    # make any.properties file
    return render(request, "masc-lab/lab.html", {
        "input_code": "NUll",
        "output_code": "Null"
    })


def update_file_content(filename, content):
    print(content)
    arr = bytes(content, 'utf-8')
    with open('./modules/static/properties/' + filename, 'wb') as destination:
        destination.write(arr)


def get_operator_type_selected_file(f):
    with open('./modules/static/properties/' + f, 'r') as destination:
        item = destination.read().split("\n")
    for line in item:
        if 'type' in line.lower():
            temp = line.split("=")
            return temp[1]
    return "no_operator"


def read_selected_file(f):
    with open('./modules/static/properties/' + f, 'r') as destination:
        item = destination.read().split("\n")
    content = ''
    for line in item:
        if 'mutantGeneration' in line or 'excludedOperators' in line or 'automatedAnalysis' in line:
            continue
        else:
            content = content + line + '\n'
    return content


def sanitize_content(initial_content):
    item = initial_content.split("\n")
    content = ''
    for line in item:
        if 'mutantGeneration' in line or 'excludedOperators' in line or 'automatedAnalysis' in content:
            continue
        else:
            content = content + line + '\n'
    return content
    # if 'automatedAnalysis' in content:
    #     return content
    # else:
    #     return 'automatedAnalysis = false' + '\n' + content


def read_file(f):
    with open('./modules/static/properties/' + f, 'r') as destination:
        contents = destination.read()
    return contents


def get_final_output(paths):
    output = ''
    for path in paths:
        with open('./' + path, 'r') as destination:
            item = destination.read()
            h = path.split('/')
            header = '=============' + h[len(h) - 2] + '================'
            output = output + '\n' + '\n' + header + '\n' + item
    return output


def read_logs():
    outputPaths = []
    with open('./MainScope.log', 'r') as destination:
        contents = destination.readlines()
    for line in contents:
        if "[OutputPath]" in line:
            x = line.split('#')
            outputPaths.append(x[len(x) - 1].strip('\n'))
    return get_final_output(outputPaths)


def input_Form(request):
    if request.method == "POST":
        properties = request.POST['properties']
        fileinput = read_selected_file(properties)
        selected_operator = get_operator_type_selected_file(properties)
        if "StringOperator" in selected_operator:
            form = StringOperatorForm
        elif "ByteOperator" in selected_operator:
            form = ByteOperatorForm
        elif "InterprocOperator" in selected_operator:
            form = InterProcOperatorForm
        elif "Flexible" in selected_operator:
            form = FlexibleOperatorForm
        elif "IntOperator" in selected_operator:
            form = IntOperatorForm
        else:
            form = NullOperatorForm
        # list_of_operators = ["StringOperator", "ByteOperator", "InterprocOperator", "Flexible", "IntOperator"]
        checkform = CheckSave
        return render(request, "masc-lab/setup.html", {
            "properties": properties,
            "content": fileinput,
            "selected_type": selected_operator,
            'form': form,
            "save_check_box": checkform,
            "assets": MASCLabAsset
        })
    records = PropertiesList.objects.filter(scope='MAIN')
    return render(request, "masc-lab/input-form.html", {
        "properties_file": records,
        "assets": MASCLabAsset
    })


def set_up(request):
    if request.method == "POST":
        properties = request.POST['selected_properties']
        file_content = request.POST['content']
        selected_operator = request.POST['type']
        excluded_operator = "empty"
        if "StringOperator" in selected_operator:
            form = StringOperatorForm(request.POST)
            if form.is_valid():
                operators = form.cleaned_data.get('Operators_List')
                excluded_operator = ''.join(operators)
        elif "ByteOperator" in selected_operator:
            form = ByteOperatorForm(request.POST)
            if form.is_valid():
                operators = form.cleaned_data.get('Operators_List')
                excluded_operator = ''.join(operators)
        elif "InterprocOperator" in selected_operator:
            form = InterProcOperatorForm(request.POST)
            if form.is_valid():
                operators = form.cleaned_data.get('Operators_List')
                excluded_operator = ''.join(operators)
        elif "Flexible" in selected_operator:
            form = FlexibleOperatorForm(request.POST)
            if form.is_valid():
                operators = form.cleaned_data.get('Operators_List')
                excluded_operator = ''.join(operators)
        elif "IntOperator" in selected_operator:
            form = IntOperatorForm(request.POST)
            if form.is_valid():
                operators = form.cleaned_data.get('Operators_List')
                excluded_operator = ''.join(operators)
        else:
            excluded_operator = "empty"
        initial = 'mutantGeneration = true' + '\n' + 'automatedAnalysis = false' + '\n' + 'excludedOperators=' + excluded_operator + '\n'
        contents = initial + sanitize_content(file_content)
        update_file_content(properties, contents)
        p = asyncio.run(
            run('java -jar ./modules/static/properties/app-all.jar ./modules/static/properties/' + properties))
        # read the output file
        input_code = read_file(properties)
        output_code = read_logs()
        stdOut = p
        return render(request, "masc-lab/lab.html", {
            "input_code": input_code,
            "output_code": output_code,
            "stdOut": stdOut,
            "assets": MASCLabAsset
        })


def get_output_paths_for_download():
    outputPaths = []
    with open('./MainScope.log', 'r') as destination:
        contents = destination.readlines()
    for line in contents:
        if "[OutputPath]" in line:
            x = line.split('#')
            path = x[len(x) - 1].strip('\n')
            h = path.split('/')
            h.pop()
            outputPaths.append("/".join(h))
    return outputPaths


def download(request):
    folders = get_output_paths_for_download()
    byte_data = BytesIO()
    zip_file = zipfile.ZipFile(byte_data, "w")

    for folder in folders:
        for dirpath, dirnames, filenames in os.walk(folder):
            for filename in filenames:
                zip_file.write(
                    os.path.join(dirpath, filename),
                    os.path.relpath(os.path.join(dirpath, filename), os.path.join(folders[0], '../..')))
    zip_file.close()

    response = HttpResponse(byte_data.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=mutation.zip'

    return response

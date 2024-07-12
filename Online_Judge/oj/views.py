from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from compiler.forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
from question.models import questions

def test(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            language = submission.language
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            # if language == "cpp":
            #     executable_path = codes_dir / unique
            #     compile_result = subprocess.run(
            #         ["gcc", str(code_file_path), "-o", str(executable_path)]
            #     )
            #     print("COMPILED \n \n")
            #     if compile_result.returncode == 0:
            #         with open(input_file_path, "r") as input_file:
            #             with open(output_file_path, "w") as output_file:
            #                 subprocess.run(
            #                     [str(executable_path)],
            #                     stdin=input_file,
            #                     stdout=output_file,
            #                 )
            if language == "py":
                # Code for executing Python script
                result = subprocess.run(
                    ["python", "-c", submission.code],
                    input = submission.input_data.encode(),
                    stdout= subprocess.PIPE,
                    stderr= subprocess.PIPE
                )
            OUTPUT = result.stdout.decode()
            print("OUTPUT : " , OUTPUT)
            submission.output_data = output
            submission.save()
            return render(request, "result.html", {"submission": submission})
    else:
        form = CodeSubmissionForm()
    return render(request, "index.html", {"form": form})


def test_oj(request, question_id):
    Resp = {}
    form = CodeSubmissionForm(request.POST)
    if not form.is_valid():
        return JsonResponse({"Status" : "Error in Form"})
    submission = form.save()
    language = submission.language
    code = submission.code
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]
    project_path = project_path / "oj"
    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)
    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    Question = questions.objects.get(pk = question_id)
    for q in Question.testcases.all():
        with open(code_file_path, "w") as code_file:
            code_file.write(code)

        with open(input_file_path, "w") as input_file:
            input_file.write(q.Input)

        with open(output_file_path, "w") as output_file:
            pass  # This will create an empty file

        if language == "cpp":
            executable_path = codes_dir / unique
            compile_result = subprocess.run(
                ["gcc", str(code_file_path), "-o", str(executable_path)]
            )
            print("COMPILED \n \n")
            if compile_result.returncode == 0:
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            [str(executable_path)],
                            stdin=input_file,
                            stdout=output_file,
                        )
        elif language == "py":
            # Code for executing Python script
            try :
                print("DONE \n \n")
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["python", str(code_file_path)],
                            stdin=input_file,
                            stdout=output_file,
                            timeout = 5
                        )
                print("DONE2 \n \n")
            except subprocess.TimeoutExpired:
                Resp["Status"] = "Timeout"
                Resp['TestCase_ID'] = q.pk
                return JsonResponse(Resp)
        # Read the output from the output file
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()
        if(output_data.strip() != q.Output):
            Resp['Status'] = 'Wrong Answer'
            Resp['TestCase_ID'] = q.pk
            return JsonResponse(Resp)
            break
    print("DONE3 /n /n")
    Resp['Status'] = 'Accepted'    
    return JsonResponse(Resp)
    pass

# def test_oj(request, question_id):
#     Result = {}
#     if request.method == "POST":
#         form = CodeSubmissionForm(request.POST)
#         q = questions.objects.get(pk=question_id)
#         if form.is_valid():
#             submission = form.save()
#             print(submission.language)
#             print(submission.code)
#             language = submission.language
#             output = run_code(
#                 submission.language, submission.code, submission.input_data
#             )
#             # if language == "cpp":
#             #     executable_path = codes_dir / unique
#             #     compile_result = subprocess.run(
#             #         ["gcc", str(code_file_path), "-o", str(executable_path)]
#             #     )
#             #     print("COMPILED \n \n")
#             #     if compile_result.returncode == 0:
#             #         with open(input_file_path, "r") as input_file:
#             #             with open(output_file_path, "w") as output_file:
#             #                 subprocess.run(
#             #                     [str(executable_path)],
#             #                     stdin=input_file,
#             #                     stdout=output_file,
#             #                 )
#             if language == "py":
#                 flag = True
#                 try :
#                     test_id = -1
#                     for testcase in q.testcases.all():
#                     # Code for executing Python script
#                         test_id = testcase.Test_ID
#                         result = subprocess.run(
#                             ["python", "-c", submission.code],
#                             input = testcase.Input.encode(),
#                             stdout= subprocess.PIPE,
#                             stderr= subprocess.PIPE,
#                             timeout= 5
#                         )
#                         Output = result.stdout.decode()
#                         print("TestCase Expected Output :", testcase.Output)
#                         print("OUTPUT : " , Output)
#                         if(Output.strip() != testcase.Output.strip()):
#                             flag = False
#                             break
#                         #submission.output_data = output
#                     # submission.save()
#                     if(flag):
#                         Result['Status'] = 'Accepted'
#                     else:
#                         Result['Status'] = 'Wrong Answer'
#                         Result['Test_ID'] = test_id
                       
#                 except subprocess.TimeoutExpired:
#                     Result['Status'] = 'Timeout'
                     
#             return JsonResponse(Result)
#             return render(request, "result.html", {"submission": submission})
#     else:
#         form = CodeSubmissionForm()
#     return render(request, "index.html", {"form": form})




def submit(request):
    if request.method == "POST":
        form = CodeSubmissionForm(request.POST)
        if form.is_valid():
            submission = form.save()
            print(submission.language)
            print(submission.code)
            output = run_code(
                submission.language, submission.code, submission.input_data
            )
            submission.output_data = output
            submission.save()
            return render(request, "result.html", {"submission": submission})
    else:
        form = CodeSubmissionForm()
    return render(request, "index.html", {"form": form})


def run_code(language, code, input_data):
    project_path = Path(settings.BASE_DIR)
    directories = ["codes", "inputs", "outputs"]

    for directory in directories:
        dir_path = project_path / directory
        if not dir_path.exists():
            dir_path.mkdir(parents=True, exist_ok=True)

    codes_dir = project_path / "codes"
    inputs_dir = project_path / "inputs"
    outputs_dir = project_path / "outputs"

    unique = str(uuid.uuid4())

    code_file_name = f"{unique}.{language}"
    input_file_name = f"{unique}.txt"
    output_file_name = f"{unique}.txt"

    code_file_path = codes_dir / code_file_name
    input_file_path = inputs_dir / input_file_name
    output_file_path = outputs_dir / output_file_name

    with open(code_file_path, "w") as code_file:
        code_file.write(code)

    with open(input_file_path, "w") as input_file:
        input_file.write(input_data)

    with open(output_file_path, "w") as output_file:
        pass  # This will create an empty file

    if language == "cpp":
        executable_path = codes_dir / unique
        compile_result = subprocess.run(
            ["gcc", str(code_file_path), "-o", str(executable_path)]
        )
        print("COMPILED \n \n")
        if compile_result.returncode == 0:
            with open(input_file_path, "r") as input_file:
                with open(output_file_path, "w") as output_file:
                    subprocess.run(
                        [str(executable_path)],
                        stdin=input_file,
                        stdout=output_file,
                    )
    elif language == "py":
        # Code for executing Python script
        with open(input_file_path, "r") as input_file:
            with open(output_file_path, "w") as output_file:
                subprocess.run(
                    ["python", str(code_file_path)],
                    stdin=input_file,
                    stdout=output_file,
                )

    # Read the output from the output file
    with open(output_file_path, "r") as output_file:
        output_data = output_file.read()

    return output_data
    
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from compiler.forms import CodeSubmissionForm
from django.conf import settings
import os
import uuid
import subprocess
from pathlib import Path
from question.models import questions
from contest.models import Submission, Contests, Score, Leaderboard
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model

User = get_user_model()

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
    flag = True
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
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["python", str(code_file_path)],
                            stdin=input_file,
                            stdout=output_file,
                            timeout = 5
                        )
            except subprocess.TimeoutExpired:
                Resp["Status"] = "Timeout"
                Resp['TestCase_ID'] = q.pk
                return JsonResponse(Resp)
        # Read the output from the output file
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()
        # print("output_data:", output_data)
        # print("testcase: ",  q.Output)
        if(output_data.strip() != q.Output):
            flag = False
            Resp['Status'] = 'Wrong Answer'
            Resp['TestCase_ID'] = q.pk
            break
    if(flag):
        Resp['Status'] = 'Accepted'    
    sub = Submission(code= code,user = request.user, question=Question, verdict = Resp['Status'], language= language)
    sub.save()
    return JsonResponse(Resp)
    pass

def contest_test_oj(request, contest_id, question_id):
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
    Contest = Contests.objects.get(pk = contest_id)
    Question = questions.objects.get(pk = question_id)
    flag = True
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
                with open(input_file_path, "r") as input_file:
                    with open(output_file_path, "w") as output_file:
                        subprocess.run(
                            ["python", str(code_file_path)],
                            stdin=input_file,
                            stdout=output_file,
                            timeout = 5
                        )
            except subprocess.TimeoutExpired:
                Resp["Status"] = "Timeout"
                Resp['TestCase_ID'] = q.pk
                return JsonResponse(Resp)
        # Read the output from the output file
        with open(output_file_path, "r") as output_file:
            output_data = output_file.read()
        # print("output_data:", output_data)
        # print("testcase: ",  q.Output)
        if(output_data.strip() != q.Output):
            flag = False
            Resp['Status'] = 'Wrong Answer'
            Resp['TestCase_ID'] = q.pk
            break
    if(flag):
        Resp['Status'] = 'Accepted'    
    sub = Submission(contest= Contest, user = request.user, question=Question, verdict = Resp['Status'], language= language)
    sub.save()
    update_score(question_id=question_id, contest_id=contest_id, user_id=request.user.pk, status = Resp['Status'])
    return JsonResponse(Resp)

def update_score(question_id, contest_id, user_id, status):
    print(status)
    user = User.objects.get(pk=user_id)
    contest = Contests.objects.get(pk = contest_id)
    question = questions.objects.get(pk = question_id)
    try :
        score = get_object_or_404(Score, user= user, question = question, contest = contest)
    except :
        score = Score(question=question, contest=contest, user = user, score =0)
        score.save()
    previous = score.score
    if(status == 'Accepted'):
        score.score = 1
        if(previous == 0):
            lbd = Leaderboard.objects.get(contest=contest, user = user)
            lbd.total_score += 1
            lbd.save()
    else :
        score.score = 0
    score.save()

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
    
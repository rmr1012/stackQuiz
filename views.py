from django.views.generic import TemplateView, View
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.http import HttpResponseForbidden , HttpResponse
from django.urls import reverse
from stackQuiz.models import *
from random import *
from stackapi import StackAPI

key="YRbWKYI*hhIRDZXXE9ijEw(("

SITE = StackAPI('electronics',key=key)
SITE.max_pages=1
SITE.page_size=100


fakeQuestion={"question":{"id":"12345","title":"who gives a fuck?","content":"lolol man this content is trash hahaha"},"answers":[{"id":"55555","votes":15,"content":"happy answer 15"},{"id":"22222","votes":5,"content":"sad answer 5"}]}
class HomeView(TemplateView): #some from 48
    template_name = 'stackQuiz/stackQuiz.html'
    def get(self, request):

        context = fakeQuestion # delete dummy when there's real stuff
        return render(request, self.template_name,context)


@api_view(['GET','POST'])
@csrf_exempt
def LoadAPI(request):

    if request.method == 'POST':
        idx=request.POST.get('idx[]')
        length=int(request.POST.get('length'))
        query=request.POST.get('query')
        print(idx)

        context=fakeQuestion
        newCard=''
        for i in range(length):
            newCard += render_to_string('stackQuiz/card.html', context)

        return JsonResponse({"card":newCard,"context":context})


@api_view(['GET','POST'])
@csrf_exempt
def SearchAPI(request):

    if request.method == 'POST':
        idx=request.POST.get('idx[]')
        query=request.POST.get('query')
        length=int(request.POST.get('length'))

        print(idx)

        questions=buildContext(query,length)
        qIDs=[]
        for question in questions:
            print(question["question"]["id"])
            qIDs.append(question["question"]["id"])
        allCards=''

        #print(questions)
        for question in questions:
            newCard = render_to_string('stackQuiz/card.html',question)
            allCards+=newCard

        return JsonResponse({"card":allCards,'ids':qIDs})
maxAns=4 # max ans per ques
def buildContext(query,length):
    searchResult=SITE.fetch("search",intitle=query,sort="relevance",order="desc",filter="!)EhwLl5mQ7SRRT.ghEE_.7mDw6z-FVdx9vSNH8IM4fdEpC-K*")

    qList=[]

    for idx,question in enumerate(searchResult["items"]):
        questionDict={}
        if question['is_answered'] and question['question_id']:
            print(question["title"])
            questionDict["id"]=question['question_id']
            questionDict["link"]=question['question_id']
            questionDict["title"]=question['title']
            questionDict["content"]=question['body']
            answerVotesList=[]

            for ansIdx,answer in enumerate(sorted(question["answers"], key = lambda i: i['up_vote_count'],reverse=True)):
                answerDict={}
                if ansIdx>maxAns:
                    break
                if answer["up_vote_count"]:
                    answerDict["votes"]=answer["up_vote_count"]
                    answerDict["title"]=answer["title"]
                    answerDict["body"]=answer["body"]
                    answerDict["id"]=answer["answer_id"]
                    answerVotesList.append(answerDict)

            qList.append({"question":questionDict,"answers":answerVotesList})
        if idx>length:
            break
    return qList

from django.shortcuts import render, redirect
from generator.models import userregister
from generator.models import helpsupport
from generator.models import myreview
import requests
from django.core.mail import send_mail
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from django.conf import settings
import random
import json
import datetime
from datetime import date
from newsapi.newsapi_client import NewsApiClient
from newsdataapi import NewsDataApiClient
from django.contrib import messages

# Create your views here.

def index(request):
	if request.session.has_key('email'):
		if request.method=="POST":
			category=request.POST.get('category')
			language=request.POST.get('language')
			sort=request.POST.get('sort')
			search=str(request.POST.get('name'))
			print(category)
			print(language)
			if category and not language and not sort:
				print(category)
				try:
					newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
					json_data= newsapi.get_everything(q=category,language='en',page=1,sort_by='relevancy')
					k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				except Exception as e:
					print(f"An error occurred while fetching the news articles: {e}")
					k = []
				return render(request,'index.html',{'logout':'logout','k':k,'fresult':'fresult'})

			if language and not category and not sort:
				print(language)
				try:
					newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
					json_data= newsapi.get_everything(q='Featured News',language=language,page=1,sort_by='relevancy')
					k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				except Exception as e:
					print(f"An error occurred while fetching the news articles: {e}")
					k = []
				try:
					newsdataapi = NewsDataApiClient(apikey="pub_4803543aad1630f176c16b82b79178ac7d53f")
					response = newsdataapi.news_api(q='Featured News',language=language)
					k2=[article for article in response['results'] if article.get('description') is not None]
				except Exception as e:
					print(f"An error occurred while fetching the news articles: {e}")
					k2 = []
				url = f'https://api.currentsapi.services/v1/latest-news?apiKey=oo1oBEjFkxw9zYAOHvPaaqf2vOwAJv3e2QEikaAt5h67Gmz9&language={language}'
				response2 = requests.get(url)
				if response2.status_code == 200:
					news_data = response2.json()
					news_list = [article for article in news_data.get('news', []) if article.get('description') is not None]
				else:
					news_list = []
					print("Failed to retrieve data")
				return render(request,'index.html',{'logout':'logout','k':k,'k2':k2,'k3':news_list,'fresult':'fresult'})


			if category and language and not sort:
				print(category)
				print(language)
				try:
					newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
					json_data= newsapi.get_everything(q=category,language=language,page=1,sort_by=sort)
					k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				except Exception as e:
					print(f"An error occurred while fetching the news articles: {e}")
					k = []
				try:
					newsdataapi = NewsDataApiClient(apikey="pub_4803543aad1630f176c16b82b79178ac7d53f")
					response = newsdataapi.news_api(category=category,language=language)
					k2=[article for article in response['results'] if article.get('description') is not None]
				except Exception as e:
					print(f"An error occurred while fetching the news articles: {e}")
					k2 = []
				url = f'https://api.currentsapi.services/v1/latest-news?apiKey=oo1oBEjFkxw9zYAOHvPaaqf2vOwAJv3e2QEikaAt5h67Gmz9&language={language}&category={category}'
				response2 = requests.get(url)
				if response2.status_code == 200:
					news_data = response2.json()
					news_list = [article for article in news_data.get('news', []) if article.get('description') is not None]
				else:
					news_list = []
					print("Failed to retrieve data")
				return render(request,'index.html',{'logout':'logout','k':k,'k2':k2,'k3':news_list,'fresult':'fresult'})

			if sort and not category and not language:
				newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
				json_data= newsapi.get_everything(q='Featured News',language='en',page=1,sort_by=sort)
				k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				return render(request,'index.html',{'logout':'logout','k':k,'fresult':'fresult'})

			if sort and category and not language:
				newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
				json_data= newsapi.get_everything(q=category,language='en',page=1,sort_by=sort)
				k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				return render(request,'index.html',{'logout':'logout','k':k,'fresult':'fresult'})

			if sort and language and not category:
				newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
				json_data= newsapi.get_everything(q='Featured News',language=language,page=1,sort_by=sort)
				k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				return render(request,'index.html',{'logout':'logout','k':k,'fresult':'fresult'})

			if sort and language and category:
				newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
				json_data= newsapi.get_everything(q=category,language=language,page=1,sort_by=sort)
				k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				return render(request,'index.html',{'logout':'logout','k':k,'fresult':'fresult'})




			if search:
				if not search.strip():
					messages.add_message(request, messages.INFO, 'wrong input')
					return redirect('index')
				newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
				json_data= newsapi.get_everything(q=search,language='en',page_size=18,page=1,sort_by='relevancy')
				k=[article for article in json_data['articles'] if '[Removed]' not in article['content']]
				newsdataapi = NewsDataApiClient(apikey="pub_4803543aad1630f176c16b82b79178ac7d53f")
				response = newsdataapi.news_api(q=search,language='en')
				k2=[article for article in response['results'] if article.get('description') is not None]
				if not k and not k2:
					messages.add_message(request, messages.INFO, 'No results found')
					return redirect('index')
				if k and not k2:
					length=len(k)
					print(length)
					if length%3==0:
						right='right'
					else:
						if length%2==0:
							right='even'
							length=len(k)-1
						else:
							right='odd'
							length=len(k)-2
					return render(request,'index.html',{'logout':'logout','ks':k,'sresult':'sresult','right':right,'length':length})
				if k2 and not k:
					return render(request,'index.html',{'logout':'logout','k2s':k2,'sresult':'sresult'})
				length=len(k)
				print(length)
				if length%3==0:
					right='right'
				else:
					if length%2==0:
						right='even'
						length=len(k)-1
					else:
						right='odd'
						length=len(k)-2
				return render(request,'index.html',{'logout':'logout','ks':k,'k2s':k2,'sresult':'sresult','length':length,'right':right})

		else:
			newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
			json_data= newsapi.get_everything(q='Featured News',language='en',page_size=18,page=1,sort_by='relevancy')
			k=json_data['articles']
			newsdataapi = NewsDataApiClient(apikey="pub_4803543aad1630f176c16b82b79178ac7d53f")
			response = newsdataapi.news_api(q="Featured News",language='en')
			k2=[article for article in response['results'] if article.get('description') is not None]
			url = 'https://api.currentsapi.services/v1/latest-news?apiKey=oo1oBEjFkxw9zYAOHvPaaqf2vOwAJv3e2QEikaAt5h67Gmz9'
			response2 = requests.get(url)
			if response2.status_code == 200:
				news_data = response2.json()
				news_list = [article for article in news_data.get('news', []) if article.get('description') is not None]
			else:
				news_list = []
				print("Failed to retrieve data")
			return render(request,'index.html',{'logout':'logout','k':k,'k2':k2,'k3':news_list})
	else:
		if request.method=="POST":
			messages.add_message(request, messages.INFO, 'error')
			return redirect('index')
		else:
			newsapi=NewsApiClient(api_key='40f8fa21da67431885edfaec3fa49ac4')
			json_data= newsapi.get_everything(q='Featured News',language='en',page_size=18,page=1,sort_by='relevancy')
			k=json_data['articles']
			newsdataapi = NewsDataApiClient(apikey="pub_4803543aad1630f176c16b82b79178ac7d53f")
			response = newsdataapi.news_api(q="Featured News",language='en')
			k2=[article for article in response['results'] if article.get('description') is not None]
			url = 'https://api.currentsapi.services/v1/latest-news?apiKey=oo1oBEjFkxw9zYAOHvPaaqf2vOwAJv3e2QEikaAt5h67Gmz9'
			response2 = requests.get(url)
			if response2.status_code == 200:
				news_data = response2.json()
				news_list = [article for article in news_data.get('news', []) if article.get('description') is not None]
			else:
				news_list = []
				print("Failed to retrieve data")
			return render(request,'index.html',{'login':'login','k':k,'k2':k2,'k3':news_list})
		


def base(request):
	return render(request,'base.html')

def nav(request):
	return render(request,'nav.html')

def footer(request):
	return render(request,'footer.html')

def about(request):
	if request.session.has_key('email'):
		all_reviews = list(myreview.objects.all())
		return render(request,'about.html',{'all_reviews':all_reviews,'logout':'logout'})
	else:
		all_reviews = list(myreview.objects.all())
		return render(request,'about.html',{'all_reviews':all_reviews,'login':'login'})

def login(request):
	if request.method=="POST":
		email=request.POST.get('email')
		password=request.POST.get('password')
		x=userregister.objects.filter(email=email,password=password)
		k=len(x)
		if k>0:
			request.session['email']=email
			return redirect('index')
		else:
			messages.add_message(request, messages.INFO, '1')
			return redirect('index')
	else:
		return render(request,'login.html',{'login':'login'})
	

def logout(request):
    del request.session['email']
    return redirect('index')







	

def register(request):
	if request.method=="POST":
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		confirm_password=request.POST.get('confirm_password')
		if userregister.objects.filter(email=email).exists():
			messages.add_message(request, messages.INFO, 'already')
			return redirect('index')
		else:
			if password==confirm_password:
				otp_length = 6
				otp = ''.join(random.choices('0123456789', k=otp_length))
				subject="Verification"
				message="Welcome to Market Fusion...your otp is "+otp
				email_from=settings.EMAIL_HOST_USER
				recipient_list=[email,]
				send_mail(subject,message,email_from,recipient_list)
				rest="OTP is sent to your respective email account....Please check"
				if request.session.has_key('email'):
					return render(request,'otp.html',{'otp':otp,'rest':rest,'first_name':first_name,'last_name':last_name,'email':email,'password':password,'logout':'logout'})
				else:
					return render(request,'otp.html',{'otp':otp,'rest':rest,'first_name':first_name,'last_name':last_name,'email':email,'password':password,'login':'login'})
			else:
				if request.session.has_key('email'):
					return render(request,'register.html',{'msg':'password','logout':'logout'})
				else:
					return render(request,'register.html',{'msg':'password','login':'login'})
	else:
		if request.session.has_key('email'):
			return render(request,'register.html',{'logout':'logout'})
		else:
			return render(request,'register.html',{'login':'login'})	

def otp(request):
	if request.method == 'POST':
		first_name=request.POST.get('first_name')
		last_name=request.POST.get('last_name')
		email=request.POST.get('email')
		password=request.POST.get('password')
		otp=request.POST.get('otp')
		e_otp=request.POST.get('e_otp')
		if otp==e_otp:
			x=userregister()
			x.first_name=request.POST.get('first_name')
			x.last_name=request.POST.get('last_name')
			x.email=request.POST.get('email')
			x.password=request.POST.get('password')
			x.save()
			message="REGISTERED SUCCESSFULLY"
			messages.add_message(request, messages.INFO, 'success')
			return redirect('index')
		else:
			message="VERIFICATION FAILED"
			messages.add_message(request, messages.INFO, 'verification')
			return redirect('index')
	else:
		if request.session.has_key('email'):
			return render(request,'otp.html',{'logout':'logout'})
		else:
			return render(request,'otp.html',{'login':'login'})

def forgot(request):
	if request.method=='POST':
		email=request.POST.get('email')
		user=userregister.objects.filter(email=email)
		if(len(user)>0):
			password=user[0].password
			subject="Password"
			message="Welcome to cyber security...your password is "+password
			email_from=settings.EMAIL_HOST_USER
			recipient_list=[email,]
			send_mail(subject,message,email_from,recipient_list)
			rest="Your password sent to your respective email account....Please check"
			if request.session.has_key('email'):
				return render(request,'forgot.html',{'rest':rest,'logout':'logout'})
			else:
				return render(request,'forgot.html',{'rest':rest,'login':'login'})
		else:
			res="THIS EMAIL ID IS NOT REGISTERED!"
			if request.session.has_key('email'):
				return render(request,'forgot.html',{'res':res,'logout':'logout'})
			else:
				return render(request,'forgot.html',{'res':res,'login':'login'})
	else:
		if request.session.has_key('email'):
			return render(request,'forgot.html',{'logout':'logout'})
		else:
			return render(request,'forgot.html',{'login':'login'})

def review(request):
	if request.session.has_key('email'):
		email = request.session['email']
		if request.method=="POST":
			x=myreview()
			x.email=request.POST.get('email')
			x.message=request.POST.get('review')
			x.save()
			msg="REVIEW ADDED SUCCESSFULLY"
			return render(request,'review.html',{'msg':msg,'logout':'logout','email':email})
		else:
			return render(request,'review.html',{'logout':'logout','email':email})
	else:
		messages.add_message(request, messages.INFO, 'error')
		return redirect('index')


def help(request):
	if request.session.has_key('email'):
		email = request.session['email']
		if request.method=="POST":
			x=helpsupport()
			x.email=request.POST.get('email')
			x.message=request.POST.get('message')
			x.save()
			msg="MESSAGE SUBMITTED SUCCESSFULLY"
			return render(request,'help.html',{'msg':msg,'logout':'logout','email':email})
		else:
			return render(request,'help.html',{'logout':'logout','email':email})
	else:
		messages.add_message(request, messages.INFO, 'error')
		return redirect('index')


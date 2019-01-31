from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, render_to_response, redirect
from django.urls import reverse
from django.views import generic
from django.template import Context, Template, loader, RequestContext
from django.conf import settings
from django.http import Http404
import requests, ast, urllib.request, smtplib, random, json
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from .functions import *
from Lunar_Lovelies.models import *
from Lunar_Lovelies.forms import *
from .forms import *

# Create your views here.

def index(request):
	template=loader.get_template('./Lunar_Lovelies/index.html')
	args={'Title': 'Home',}
	return render(request, './Lunar_Lovelies/index.html', args)

def products_page(request):
	if request.method == 'POST':
		if 'product_filter' in request.POST:
			product_filter=ProductFilterForm(request.POST)
			product_filter.is_valid()
			filtered_products=None
			if product_filter.cleaned_data['clothes']== True or product_filter.cleaned_data['dresses']== True or product_filter.cleaned_data['shirts']== True or product_filter.cleaned_data['crafts'] == True:
				if product_filter.cleaned_data['clothes'] == True:
					clothes=products.objects.filter(category__contains="clothes")
					if filtered_products:
						filtered_products=filtered_products | clothes
					else:
						filtered_products=clothes
				if product_filter.cleaned_data['dresses'] == True:
					dresses=products.objects.filter(category__contains="dresses")
					if filtered_products:
						filtered_products=filtered_products | dresses
					else:
						filtered_products=dresses
				if product_filter.cleaned_data['shirts'] == True:
					shirts=products.objects.filter(category__contains="shirts")
					if filtered_products:
						filtered_products=filtered_products | shirts
					else:
						filtered_products=shirts
				if product_filter.cleaned_data['crafts'] == True:
					crafts=products.objects.filter(category__contains="crafts")
					if filtered_products:
						filtered_products=filtered_products | crafts
					else:
						filtered_products=crafts
				form=product_filter
				products_list=''
				for product in filtered_products:
					products_list=products_list+product_adder(product)
				args={'products_list': products_list, 'form': form, 'Title': 'Products', 'product_matches': filtered_products, 'collection_name': 'none'}
				template=loader.get_template('./Lunar_Lovelies/products_page.html')
				return render(request, './Lunar_Lovelies/products_page.html', args)
			else:
				all_products=products.objects.all()
				products_list=''
				for product in all_products:
					products_list=products_list+product_adder(product)
				form=ProductFilterForm()
				args={'form': form, 'products_list': products_list, 'Title': 'Products', 'product_matches': all_products, 'collection_name': 'none'}
				template=loader.get_template('./Lunar_Lovelies/products_page.html')
				return render(request, './Lunar_Lovelies/products_page.html', args)
		
	else:
		all_products=products.objects.all()
		products_list=''
		for product in all_products:
			products_list=products_list+product_adder(product)
		form=ProductFilterForm()
		args={'form': form, 'products_list': products_list, 'Title': 'Products', 'product_matches': all_products, 'collection_name': 'none', 'filters':'', 'sorter':'None'}
		template=loader.get_template('./Lunar_Lovelies/products_page.html')
		return render(request, './Lunar_Lovelies/products_page.html', args)

def collections(request, collection_name):
#need to put in a 'if request.method=post' here for the filter

	#Uses the collection name in order to filter by category and display products in that category
	products_list, collection_list=get_collection_products(collection_name)
	args={'products_list': products_list, 'Title': 'Products', 'product_matches': collection_list, 'collection_name': collection_name, 'filters':'', 'sorter':'None'}
	template=loader.get_template('./Lunar_Lovelies/products_page.html')
	return render(request, './Lunar_Lovelies/products_page.html', args)

def filter(request, collection_name, filters):
	#Used to filter the collection down based on the available filters
	products_list, collection_list=get_collection_products(collection_name)
	filter_list=parse_filters(filters)
	filtered_products=None
	for each_filter in filter_list:
		temp=collection_list.filter(filters__contains=each_filter)
		if filtered_products:
			filtered_products=filtered_products | temp
		else:
			filtered_products=temp
	products_list=''
	for product in filtered_products:
		products_list=products_list+product_adder(product)
	args={'products_list': products_list, 'Title': 'Filtered Products', 'product_matches': filtered_products, 'collection_name': collection_name, 'filters': filters, 'sorter':'None'}
	template=loader.get_template('./Lunar_Lovelies/products_page.html')
	return render(request, './Lunar_Lovelies/products_page.html', args)

def sortProducts(request, collection_name, sortFilter, filters=None):
	products_list, collection_list=get_collection_products(collection_name)
	if sortFilter=='price-low-high':
		sorted_products=collection_list.order_by('price')
	elif sortFilter=='price-high-low':
		sorted_products=collection_list.order_by('-price')
	elif sortFilter=='new-old':
		sorted_products=collection_list.order_by('date_added')
	elif sortFilter=='old-new':
		sorted_products=collection_list.order_by('-date_added')

	if filters:
		filter_list=parse_filters(filters)
		filtered_products=None
		for each_filter in filter_list:
			temp=sorted_products.filter(filters__contains=each_filter)
			if filtered_products:
				filtered_products=filtered_products | temp
			else:
				filtered_products=temp
		sorted_products=filtered_products

	products_list=''
	for product in sorted_products:
		products_list=products_list+product_adder(product)
	args={'products_list': products_list, 'Title': 'Sorted Products', 'product_matches': sorted_products, 'collection_name': collection_name, 'filters': filters, 'sorter': sortFilter}
	template=loader.get_template('./Lunar_Lovelies/products_page.html')
	return render(request, './Lunar_Lovelies/products_page.html', args)

def individual_product_page(request, product_name):
	revised_product_name=''
	#Translates the URL to the initial product name
	for char in product_name:
		if char=="-":
			revised_product_name=revised_product_name+' '
		else:
			revised_product_name=revised_product_name+char
	try:
		products.objects.filter(name=revised_product_name).exists()
	except:
		raise Http404
	product=products.objects.get(name=revised_product_name)
	#URL used to get user back from paypal
	return_url='http://127.0.0.1:8000/products/'+product_name
	template=loader.get_template('./Lunar_Lovelies/individual_product_page.html')
	args={'product':product,'picture_url':product.picture_url, 'name':revised_product_name, 'price':product.price, 'return_url': return_url, 'Title': revised_product_name, 'paypal_button': product.paypal_button}
	return render(request, './Lunar_Lovelies/individual_product_page.html', args)

def product_search(request):
	product_query=request.GET.get('query')
	category_search=products.objects.filter(category__contains=product_query)
	name_search=products.objects.filter(name__contains=product_query)
	description_search=products.objects.filter(description__contains=product_query)
	product_matches=category_search | name_search | description_search
	products_list=''
	for product in product_matches:
		products_list=products_list+product_adder(product)
	print(products_list)
	if products_list=='':
		print('product list empty')
		products_list="<p>I'm sorry, we weren't able to find any products that matched that description. If you think we should, though, please let us know!</p>"
	args={'products_list': products_list, 'Title': 'Search Results for '+product_query, 'product_matches': product_matches}
	template=loader.get_template('./Lunar_Lovelies/product_search.html')
	return render(request, './Lunar_Lovelies/product_search.html', args)

def contact(request):
	template=loader.get_template('./Lunar_Lovelies/contact.html')
	args={'Title': 'Contact Us',}
	return render(request, './Lunar_Lovelies/contact.html', args)

def about(request):
	template=loader.get_template('./Lunar_Lovelies/about.html')
	args={'Title': 'About Us',}
	return render(request, './Lunar_Lovelies/about.html', args)

#Any subscription request is routed here for verification and response
def subscribe(request):
	form=SubscribeForm(request.POST)
	if form.is_valid():
		email=form.cleaned_data.get('email_address')
		#Sends request to mailgun to add email to mailing list
		response=add_list_member(email)
		verification=json.loads(response.text)
		if verification['member']['subscribed']:
			message="Thank you for subscribing to our newsletter. We are always happy to connect with our customers and we can't to let you know about what we are working on!"
		else:
			message="Oops. Something went wrong. It seems we couldn't add you to our mailing list. Check your email and try again. It is also possible you have already subscribed before. If you think something is wrong, let us know at our Contact Page."
		args={'message': message,}
		template=loader.get_template('./Lunar_Lovelies/subscription.html')
		return render(request, './Lunar_Lovelies/subscription.html', args)

def contact_mailer(request):
	form=ContactMailer(request.POST)
	if form.is_valid():
		from_email=form.cleaned_data.get('email_address')
		message=form.cleaned_data.get('contact_message')
		#Create container for message
		msgRoot=MIMEMultipart('related')
		msgRoot['From']='do-not-reply@ryan-mooney.com'
		msgRoot['To']='mooneyryanj@gmail.com'
		msgRoot['Subject']='Contact-Us Message'
		msgText=MIMEText('Message from: '+from_email+'<br>'+message, 'html')
		msgRoot.attach(msgText)
		#Send message via smtp server
		smtp = smtplib.SMTP(host=settings.LL_EMAIL_HOST_CONTACT, port=settings.LL_EMAIL_PORT_CONTACT)
		smtp.starttls()
		smtp.login(settings.LL_EMAIL_HOST_USER_CONTACT, settings.LL_EMAIL_HOST_PASSWORD_CONTACT)
		smtp.sendmail(settings.LL_EMAIL_HOST_USER_CONTACT, 'mooneyryanj@gmail.com', msgRoot.as_string())
		smtp.quit()
	#Reinitialize page with message-sent text
	template=loader.get_template('./Lunar_Lovelies/contact.html')
	confirmation_text="Your message has been successfully sent!"
	args={'Title': 'Contact Us', 'message_confirmation': confirmation_text}
	return render(request, './Lunar_Lovelies/contact.html', args)

def product_adder(product):
	if product.out_of_stock==True:
		price='<p class="product-list-text out-of-stock">OUT OF STOCK</p>'
	else:
		price='<p class="product-list-text">$'+str(product.price)+'</p>'
	return '<div class="products-outerdiv"><li class="products-li"><div class="products-innerdiv"><a class="product-link" id="product-link" href=/LunarLovelies/products/'+product.name+'><img src="'+product.picture_url+'" class="product-image">'+'<p class="product-list-text">'+product.name+'</p>'+price+'</a></div></li></div>'

def send_to_list():
	return requests.post(
		"https://api.mailgun.net/v3/do-not-reply.ryan-mooney.com/messages",
		auth=("api", settings.MAILGUN_API),
		data={"from": "Ryan Mooney <do-not-reply@ryan-mooney.com>",
			"to": [settings.MAILING_LIST],
			"subject": "Hello",
			"text": "Testing some Mailgun awesomness!"})

def add_list_member(email):
    return requests.post(
        "https://api.mailgun.net/v3/lists/mailing-test-list@do-not-reply.ryan-mooney.com/members",
        auth=('api', settings.MAILGUN_API),
        data={'subscribed': True,
              'address': email,})

def get_collection_products(collection_name):
	collection_list=products.objects.filter(category__contains=collection_name)
	products_list=''
	for product in collection_list:
		products_list=products_list+product_adder(product)
	return products_list, collection_list

def parse_filters(filter_string):
    running_filter=''
    filter_list=[]
    for c in filter_string:
        if c=="+":
            filter_list.append(running_filter)
            running_filter=''
        else:
            if c=="-":
                running_filter=running_filter+' '
            else:
                running_filter=running_filter+c
    return filter_list
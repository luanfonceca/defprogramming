from django.template import Context, loader, RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from quotes.models import Author, Tag, Quote
from quotes.forms import QuoteForm

def index(request):
  quotes = Quote.objects.all().order_by('-publish_date')
  quotes = __validates_pagination(request, Paginator(quotes, 10))
  title = "def programming: quotes about coding"
  description = "Quotes about programming, coding, computer science, debugging, software industry, startups and motivation."
  return render_to_response('quotes/index.html', locals(), context_instance=RequestContext(request))

def detail(request, slug):
  quote = get_object_or_404(Quote, slug=slug)
  return render_to_response('quotes/detail.html', locals(), context_instance=RequestContext(request))

def random(request):
  quote = Quote.objects.order_by('?')[0]
  return render_to_response('quotes/detail.html', locals(), context_instance=RequestContext(request))

def authors(request):
  authors = Author.objects.all().order_by('name')
  title = "Listing all authors | def programming"
  description = "List of all the authors with quotes published. Quotes about programming, coding, software industry.";
  return render_to_response('quotes/authors.html', locals(), context_instance=RequestContext(request))

def author_detail(request, slug):
  author = get_object_or_404(Author, slug=slug)
  quotes = author.quote_set.all().order_by('-publish_date')
  quotes = __validates_pagination(request, Paginator(quotes, 10))
  title = "Programming quotes by %s | def programming" % author.name
  description = "Listing all programming quotes by %s. Quotes about programming, coding, software industry."  % author.name
  return render_to_response('quotes/author_detail.html', locals(), context_instance=RequestContext(request))

def tags(request):
  tags = Tag.objects.all().order_by('name')
  title = "Listing all tags | def programming"
  description = "Tags list. Quotes about programming, coding, software industry.";
  return render_to_response('quotes/tags.html', locals(), context_instance=RequestContext(request))

def tag_detail(request, slug):
  tag = get_object_or_404(Tag, slug=slug)
  quotes = tag.quote_set.all().order_by('-publish_date')
  quotes = __validates_pagination(request, Paginator(quotes, 10))
  title = "Programming quotes tagged under %s | def programming" % tag.name
  description = "Listing all programming quotes tagged under %s. Quotes about programming, coding, software industry." % tag.name
  return render_to_response('quotes/tag_detail.html', locals(), context_instance=RequestContext(request))

def submit_quote(request):
  title = "Submit a quote | def programming"
  description = "Use this form to submit a quote. Please send only quotes about programming, coding, software industry."
  sent = False
  form = QuoteForm(request.POST or None)
  if form.is_valid():
      form.save()
      messages.success(request, "Your quote was successfully submitted, thank you! :-)")
  return render_to_response('quotes/submit_quote.html', locals(), context_instance=RequestContext(request))

def __validates_pagination(request, paginator):
  page = request.GET.get('page', 1)
  try:
    return paginator.page(page)
  except PageNotAnInteger:
    return paginator.page(1)
  except EmptyPage:
    return paginator.page(paginator.num_pages)

import datetime
import pytz
from random import randint, choice

from django.http import Http404
from django.db import connection
from django.db.models.aggregates import Count

from dispatch.models import Article, Page, Section

from ubyssey.events.models import Event

class ArticleHelper(object):
    @staticmethod
    def get_article(request, slug):
        """If the url requested includes the querystring parameters 'version' and 'preview_id',
        get the article with the specified version and preview_id.

        Otherwise, get the published version of the article.
        """
        return Article.objects.get(request=request, slug=slug, is_published=True)

    @staticmethod
    def get_reading_time(article):
        word_count = 0
        words_per_min = 150
        for block in article.content:
            if block['type'] == 'paragraph':
                word_count += len(block['data'].split(' '))

        reading_time = word_count / words_per_min
        return reading_time

    @staticmethod
    def insert_ads(content, article_type='desktop'):
        """Inject upto 5 ads evenly throughout the article content.
        Ads cannot inject directly beneath headers."""
        ad = {
            'type': 'ad',
            'data': article_type
        }

        paragraph_count = 1

        for block in content:
            paragraph_count = len(filter(lambda b: b['type'] == 'paragraph', content))

        number_of_ads = 1
        paragraphs_per_ad = 6

        while paragraph_count / number_of_ads > paragraphs_per_ad :
            number_of_ads += 1
            if number_of_ads >= 5:
                paragraphs_per_ad = paragraph_count // number_of_ads
                break

        ad_count = 0
        paragraph_count = 0
        next_ad = randint(paragraphs_per_ad - 2, paragraphs_per_ad + 2)
        ad_placements = content

        for index, block in enumerate(content):
            if block['type'] == 'paragraph':
                paragraph_count += 1
            if paragraph_count == next_ad:
                    if index != 0 and content[index - 1]['type'] != 'header':
                        ad_placements.insert(index + ad_count, ad)
                        next_ad += randint(paragraphs_per_ad - 2, paragraphs_per_ad + 2)
                        ad_count += 1
                    else:
                        next_ad += 1

        return ad_placements

    @staticmethod
    def get_frontpage(reading_times=None, section=None, section_id=None, sections=[], exclude=[], limit=7, is_published=True, max_days=14):

        if is_published:
            is_published = 1
        else:
            is_published = 0

        if reading_times is None:
            reading_times = {
                'morning_start': '9:00:00',
                'midday_start': '11:00:00',
                'midday_end': '16:00:00',
                'evening_start': '16:00:00',
            }

        context = {
            'section': section,
            'section_id': section_id,
            'excluded': ",".join(map(str, exclude)),
            'sections': ",".join(sections),
            'limit': limit,
            'is_published': is_published,
            'max_days': max_days
        }

        context.update(reading_times)

        query = """
            SELECT *, TIMESTAMPDIFF(SECOND, published_at, NOW()) as age,
            CASE reading_time
                 WHEN 'morning' THEN IF( CURTIME() < %(morning_start)s, 1, 0 )
                 WHEN 'midday'  THEN IF( CURTIME() >= %(midday_start)s AND CURTIME() < %(midday_end)s, 1, 0 )
                 WHEN 'evening' THEN IF( CURTIME() >= %(evening_start)s, 1, 0 )
                 ELSE 0.5
            END as reading,
            TIMESTAMPDIFF(DAY, published_at, NOW()) <= %(max_days)s as age_deadline
            FROM dispatch_article
        """

        query_where = """
            WHERE head = 1 AND
            is_published = %(is_published)s AND
            parent_id NOT IN (%(excluded)s)
        """

        if section is not None:
            query += """
                INNER JOIN dispatch_section on dispatch_article.section_id = dispatch_section.id AND dispatch_section.slug = %(section)s
            """
        elif section_id is not None:
            query_where += " AND section_id = %(section_id)s "
        elif sections:
            query_where += "AND section_id in (SELECT id FROM dispatch_section WHERE FIND_IN_SET(slug,%(sections)s))"

        query += query_where + """
            ORDER BY age_deadline DESC, reading DESC, ( age * ( 1 / ( 4 * importance ) ) ) ASC
            LIMIT %(limit)s
        """

        return list(Article.objects.raw(query, context))

    @staticmethod
    def get_frontpage_sections(exclude=None):

        exclude = exclude or []
        results = {}

        sections = Section.objects.all()

        for section in sections:
            articles = Article.objects.exclude(id__in=exclude).filter(section=section,is_published=True).order_by('-published_at').select_related()[:5]
            if len(articles):
                results[section.slug] = {
                    'first': articles[0],
                    'stacked': articles[1:3],
                    'bullets': articles[3:],
                    'rest': articles[1:4],
                }

        return results

    @staticmethod
    def get_reading_list(article, ref=None, dur=None):
        if ref is not None:
            if ref == 'frontpage':
                articles = ArticleHelper.get_frontpage(exclude=[article.parent_id])
                name = 'Top Stories'
            elif ref == 'popular':
                articles = ArticleHelper.get_popular(dur=dur).exclude(pk=article.id)[:5]
                name = "Most popular this week"
        else:
            articles = article.get_related()
            name = article.section.name

        return {
            'ids': ",".join([str(a.parent_id) for a in articles]),
            'name': name
        }

    @staticmethod
    def get_years():
        publish_dates = Article.objects.filter(is_published=True).dates('published_at','year',order='DESC')
        years = []

        for publish_date in publish_dates:
            years.append(publish_date.year)

        return years

    @staticmethod
    def get_topic(topic_name):

        return Article.objects.filter(
            is_published=True,
            topic__name=topic_name
        )

    @staticmethod
    def is_explicit(article):
        explicit_tags = ['sex', 'explicit']
        tags = article.tags.all().values_list('name', flat=True)
        for tag in tags:
            if tag.lower() in explicit_tags:
                return True
        return False

    @staticmethod
    def get_random_articles(n, section, exclude=None):
        """Returns `n` random articles from the given section."""

        # Get all articles in section
        queryset = Article.objects.filter(is_published=True, section__slug=section)

        # Exclude article (optional)
        if exclude:
            queryset = queryset.exclude(id=exclude)

        # Get article count
        count = queryset.aggregate(count=Count('id'))['count']

        # Get all articles
        articles = queryset.all()

        # Force a query (to optimize later calls to articles[index])
        list(articles)

        results = []
        indices = set()

        # n is bounded by number of articles in database
        n = min(count, n)

        while len(indices) < n:
            index = randint(0, count - 1)

            # Prevent duplicate articles
            if index not in indices:
                indices.add(index)
                results.append(articles[index])

        return results

    @staticmethod
    def get_popular(dur='week'):
        """Returns the most popular articles in the time period."""

        durations = {
            'week': 7,
            'month': 30
        }

        articles = Article.objects.filter(is_published=True)

        if dur in durations:
            end = datetime.datetime.now() + datetime.timedelta(days=1)
            start = end - datetime.timedelta(days=durations[dur])
            time_range = (start, end)
            articles = articles.filter(created_at__range=(time_range))

        return articles.order_by('-views')

    @staticmethod
    def get_breaking_news():
        """Returns breaking news stories"""
        return Article.objects.filter(is_published=True, is_breaking=True, breaking_timeout__gte=datetime.datetime.now())

    @staticmethod
    def get_trending():
        """Returns the most trending articles in the time period."""

        DURATION = 6

        articles = Article.objects.filter(is_published=True)

        end = datetime.datetime.now()
        start = end - datetime.timedelta(hours=DURATION)
        time_range = (pytz.utc.localize(start), pytz.utc.localize(end))
        trending_articles = articles.filter(
            published_at__range=(time_range),
            views__gt=1000)

        if len(trending_articles) == 0:
            trending_article = None
        else:
            trending_article = choice(trending_articles)

        return trending_article

    @staticmethod
    def get_meta(article, default_image=None):
        try:
            image = article.featured_image.image.get_medium_url()
        except:
            image = default_image

        return {
            'title': article.headline,
            'description': article.seo_description if article.seo_description is not None else article.snippet,
            'url': article.get_absolute_url,
            'image': image,
            'author': article.get_author_type_string()
        }

class PageHelper(object):
    @staticmethod
    def get_page(request, slug):
        """If the url requested includes the querystring parameters 'version' and 'preview_id',
        get the page with the specified version and preview_id.

        Otherwise, get the published version of the page.
        """

        return Page.objects.get(request=request, slug=slug, is_published=True)

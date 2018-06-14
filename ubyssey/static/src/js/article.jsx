import React from 'react';
import './modules/Youtube';
import ArticleList from './components/ArticleList.jsx';
import Search from './components/Search.jsx';
import Poll from './components/Poll/Poll.jsx';

window.articleHeader = false;

const BOX_HEIGHT = 300
const SKYSCRAPER_HEIGHT = 624

$(function () {
    $('.c-widget-poll').each(function () {
        React.render(
            <Poll id={$(this).data('id')} loaderHTML={$(this).html()} />,
            $(this).get(0)
        )
    })
});

if ($('main.article').length) {

    const $article = $('article');

    var articleId = $article.data('id');
    var articleHeadline = $article.data('headline');
    var articleURL = $article.data('url');

    var userId = $article.data('user-id');

    var articleIds = $article.data('list');
    var listName = $article.data('list-name');
    if (articleIds === parseInt(articleIds, 10)) {
        articleIds = [articleIds];
    } else {
        articleIds = articleIds.split(',');
    }

    var firstArticle = {
        id: articleId,
        headline: articleHeadline,
        url: articleURL
    };

    function removeSidebar() {
        $('.sidebar').remove()
    }

    function removeSidebarAd() {
        $('.sidebar').children('.o-advertisement--box').removeClass('o-advertisement--box')
    }

    function stickyAds(scrollTop, headerHeight, sidebarOffset, scrollDistance, stickyElements) {

        stickyElements.map(element => {
            // adjust when skyscraper is served
            if (element.height !== $(element.element).height() && element.index != stickyElements.length - 1) {
                element.heightChange += $(element.element).height() - element.height
                element.height = $(element.element).height()
            }

            const dropoff = element.offset + scrollDistance + headerHeight - element.heightChange

            const pickup = element.offset - headerHeight

            const articleBottom = $('#content-wrapper').scrollTop() + $('.article-content').offset().top + $('.article-content').outerHeight() - element.height

            // Dropoff bottom
            if (scrollTop > dropoff || scrollTop > articleBottom) {
                if (!element.dropoff) {
                    element.dropoff = scrollTop - sidebarOffset
                }
                const topOffset = String(element.dropoff + headerHeight) + 'px'
                // const topOffset = String( element.dropoff ) + 'px'
                element.element.css('position', 'absolute')
                element.element.css('top', topOffset)
            }
            // Pickup
            else if (scrollTop > pickup) {
                if (!element.pickup) {
                    element.pickup = pickup
                }

                const topOffset = String(headerHeight) + 'px'
                element.element.css('position', 'fixed')
                element.element.css('top', topOffset)
            }
            // Dropoff top last element
            else {
                const topOffset = String(element.offset - sidebarOffset) + 'px'
                element.element.css('position', 'absolute')
                element.element.css('top', topOffset)
            }
        })
    }


    function articleAds() {
        $(function () {
            const paragraphs = $(`#article-${articleId} .article-content > p`);
            const windowHeight = $(window).height();

            // // Mobile
            if ($(window).width() < 960) {
                // do mobile stuff
            }
            // Desktop
            else {
                if ($('.article-content').height() < $('.sidebar').height()) {
                    removeSidebar();
                }

                console.log($('.article-content').height(), $('.sidebar').height())

                // Setup sticky ads
                const headerHeight = $('.topbar').height() + parseInt($('.sidebar').css('margin-top'), 10)
                const sidebarOffset = $('.sidebar').offset().top + $('#content-wrapper').scrollTop()
                const scrollDistance = ($('.article-content').height() - $('.sidebar').height()) / 2
                let stickyElements = []
                $('.sidebar').children('[class*="o-advertisement--"]').addClass('js-sticky')

                $('.js-sticky').each(function (index) {
                    const element = {
                        element: $(this),
                        index: index,
                        offset: $(this).offset().top + $('#content-wrapper').scrollTop() + index * scrollDistance + index * 100,
                        pickup: null,
                        dropoff: null,
                        height: $(this).height(),
                        heightChange: 0
                    }
                    stickyElements.push(element)
                })

                // Sticky Ads
                $('#content-wrapper').scroll(() => {
                    const scrollTop = $('#content-wrapper').scrollTop();

                    stickyAds(scrollTop, headerHeight, sidebarOffset, scrollDistance, stickyElements)
                })
            }
        })
    }

    articleAds()

    // var articleList = React.render(
    //     <ArticleList breakpoint={960} name={listName} firstArticle={firstArticle} articles={articleIds} userId={userId} />,
    //     document.getElementById('article-list')
    // );
}

React.render(
    <Search />,
    document.getElementById('search-form')
);
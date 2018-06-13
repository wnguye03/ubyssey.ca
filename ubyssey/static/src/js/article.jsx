import React from 'react';
import './modules/Youtube';
import ArticleList from './components/ArticleList.jsx';
import Search from './components/Search.jsx';
import Poll from './components/Poll/Poll.jsx';
import AdblockSplash from './components/AdblockSplash.jsx'

window.articleHeader = false;

const BOX_HEIGHT = 300
const SKYSCRAPER_HEIGHT = 600

$(function() {
    $('.c-widget-poll').each(function() {
        React.render(
            <Poll id={$(this).data('id')} loaderHTML={$(this).html()} />,
            $(this).get(0)
        )
    })
});

$(document).ready(function() {
    $('#adblock-splash').each(function() {
        React.render(
            <AdblockSplash />,
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
    if(articleIds === parseInt(articleIds, 10)){
        articleIds = [articleIds];
    } else {
        articleIds = articleIds.split(',');
    }
    var firstArticle = {
        id: articleId,
        headline: articleHeadline,
        url: articleURL
    };

    // function injectSidebarAd(sidebarAds, version, number, index, adType) {
    //     /* !!!Important!!!
    //      * Ensure Production is enabled before deploying to live site
    //     /*
        
    //     /* Production */
    //     // const id = `div-gpt-ad-1443288719995-${number}-${articleId}`;
    //     // var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement o-advertisement--box o-advertisement--center"><div class="adslot" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
        
    //     /* Test */
    //     const id = `div-${number}-${articleId}`;
            
    //     var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement ' + adType + ' o-advertisement--center"><div class="adslot-test" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
        
    //     // if (!$(`#${id}`).length) {
    //     //     $(adString).insertAfter(paragraphs.get(index));
    //     // }

    // }

    function removeSidebarAd() {
        $('.sidebar').children('.o-advertisement--box').removeClass('o-advertisement--box')
    }

    function useSkyscraper() {
        $('.sidebar').children('.o-advertisement--box').addClass('o-advertisement--skyscraper').removeClass('o-advertisement--box')
    }

    function stickyAds(scrollTop, windowHeight, headerHeight, sidebarMarginTop, sidebarOffset, stickyElements, scrollDistance) {
        
        stickyElements.map( (stickyElement, index) => {
            // console.log(scrollTop, stickyElement.offset)
            const stickyElementHeight = $(stickyElement.element).height()

            const dropoff = stickyElement.offset + scrollDistance*windowHeight
            const pickup = scrollTop + headerHeight + sidebarMarginTop
            
            // console.log('scroll', scrollTop, 'elementHeight', stickyElementHeight, 'dropoff', dropoff, 'sidebarOffset', sidebarOffset)
            
            // //check last stickyelement to see if there is space for another one
            // if (stickyElements.length - 1 === index) {
            //     if ($('.article-content').height() > dropoff + stickyElement.height + BOX_HEIGHT) {
            //         injectSidebarAd('A', index, index, 'o-advertisement--box')
            //     }
            // }

            // Dropoff bottom
            if (scrollTop > dropoff) {
                if (!stickyElement.dropoff) {
                    stickyElement.dropoff = scrollTop - sidebarOffset + headerHeight + sidebarMarginTop
                }

                const topOffset = String( stickyElement.dropoff ) + 'px'
                stickyElement.element.css('position', 'absolute')
                stickyElement.element.css('margin-top', topOffset)
            } 
            // Pickup
            else if (pickup > stickyElement.offset) {
                if (!stickyElement.pickup) {
                    stickyElement.pickup = pickup
                }
                
                const topOffset = String(headerHeight + sidebarMarginTop) + 'px'
                stickyElement.element.css('position', 'fixed')
                stickyElement.element.css('margin-top', topOffset)
                stickyElement.element.css('top', 0)
            } 
            // Dropoff top
            else {
                stickyElement.element.css('position', 'static')
                stickyElement.element.css('margin-top', 0)
            }
        })
    }

    function injectInlineAds(paragraphs, version, number, index, adType) {
        /* !!!Important!!!
            * Ensure Production is enabled before deploying to live site
        /*
        
        /* Production */
        const id = `div-gpt-ad-1443288719995-${number}-${articleId}`;
        var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement ' + adType + ' o-advertisement--center"><div class="adslot" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
        
        /* Test */
        // const id = `div-${number}-${articleId}`;
        // var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement ' + adType + ' o-advertisement--center"><div class="adslot-test" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
        
        if (!$(`#${id}`).length) {
            $(adString).insertAfter(paragraphs.get(index));
        }
    }

    function articleAds() {
        $(function() {
            const paragraphs = $(`#article-${articleId} .article-content > p`);
            const windowHeight = $(window).height();

            // Mobile
            if ($(window).width() < 960) {
                let insertIndex = Math.floor((Math.random() * 3) + 3);
                $(paragraphs).each(function(index) {
                    if(index === insertIndex) {
                        insertIndex += Math.floor((Math.random() * 3) + 3);
                        
                        if(insertIndex % 2 === 0 ) {
                            injectInlineAds(paragraphs, 'A', 99 + index, index, 'o-advertisement--mobile-leaderboard')
                        } else {
                            injectInlineAds(paragraphs, 'B', 100 + index, index, 'o-advertisement--mobile-leaderboard')
                        }
                    }
                });
            } 
            // Desktop
            else {
                $( window ).on( "load", function() {
                    // Setup sticky ads
                    const headerHeight = $('.topbar').height();
                    const sidebarOffset = $('.sidebar.offset').offset().top + $('#content-wrapper').scrollTop()
                    const sidebarMarginTop = parseInt($('.sidebar.offset').css('margin-top'), 10)
                    let stickyElements = []
                    const scrollDistance = 1
                    
                    //check if windowheight can take 
                    if ($('.article-content').height() < sidebarOffset + BOX_HEIGHT) {
                        removeSidebarAd();
                    }
                    if ($('.article-content').height() > sidebarOffset + SKYSCRAPER_HEIGHT && windowHeight > 800) {
                        useSkyscraper();
                    }
                    // const sidebarAds = Math.floor($('.article-content').height() / (sidebarOffset + SKYSCRAPER_HEIGHT + scrollDistance*windowHeight))
                    // for (let i = 0; i < sidebarAds; i++) {
                    //     const id = `div-gpt-ad-1443288719995-sidebar-${i}-${articleId}`;
                    //     $('.sidebar').children('[class*="o-advertisement--"]').append("<div class='o-advertisement js-sticky o-advertisement--box js-sticky'><div class='adslot-test' id=''></div>")
                    // } 

                    $('.sidebar').children('[class*="o-advertisement--"]').addClass('js-sticky')

                    $('.js-sticky').each(function() {
                        const stickyElement = {
                            element : $(this),
                            offset : $(this).offset().top + $('#content-wrapper').scrollTop(),
                            pickup : null,
                            dropoff : null,
                        }
                        stickyElements.push(stickyElement)
                    })

                    console.log('offsets calculated!')
                    
                    // Sticky Ads
                    $('#content-wrapper').scroll(() => {
                        const scrollTop = $('#content-wrapper').scrollTop();

                        stickyAds(scrollTop, windowHeight, headerHeight, sidebarMarginTop, sidebarOffset, stickyElements, scrollDistance)
                    })

                    // Inline Ads
                    // First inline ad should be after dropoff of sticky
                    let insertIndex = Math.floor((Math.random() * 3) + 3);
                    let count = 1;
                    $(paragraphs).each(function(index) {
                        if($(paragraphs.get(index)).offset().top + $('.content-wrapper').scrollTop() > count*windowHeight + 300) {
                            count += 1
                            console.log(count)
                            
                            if(count % 2 === 0 ) {
                                injectInlineAds(paragraphs, 'A', 99 + index, index + 1, 'o-advertisement--banner')
                            } else {
                                injectInlineAds(paragraphs, 'B', 100 + index, index + 1, 'o-advertisement--banner')
                            }
                        }
                    });

                })
            }
        })
    }
    
    articleAds()
    
    var articleList = React.render(
        <ArticleList breakpoint={960} name={listName} firstArticle={firstArticle} articles={articleIds} userId={userId} />,
        document.getElementById('article-list')
    );
}

React.render(
    <Search />,
    document.getElementById('search-form')
);
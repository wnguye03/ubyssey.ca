import React from 'react';
import './modules/Youtube';
import ArticleList from './components/ArticleList.jsx';
import Search from './components/Search.jsx';

window.articleHeader = false;

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

    function injectInlineAds() {
        $(function() {
            const paragraphs = $(`#article-${articleId} .article-content > p`);
            const windowHeight = $(window).height();

            function injectAd(version, number, index) {
                /* !!!Important!!!
                    * Ensure Production is enabled before deploying to live site
                /*
                
                /* Production */
                // const id = `div-gpt-ad-1443288719995-${number}-${articleId}`;
                // var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement o-advertisement--box o-advertisement--center"><div class="adslot" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
                
                /* Test */
                const id = `div-${number}-${articleId}`;
                var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement o-advertisement--box o-advertisement--center"><div class="adslot-test" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';
                
                if (!$(`#${id}`).length) {
                    $(adString).insertAfter(paragraphs.get(index));
                }
            }

            // Mobile
            if ($(window).width() < 960) {
                let insertIndex = Math.floor((Math.random() * 3) + 3);
                let lastIndex = null
                $(paragraphs).each(function(index) {
                    if(index === insertIndex) {
                        lastIndex = insertIndex
                        insertIndex += Math.floor((Math.random() * 3) + 3);
                        console.log(insertIndex, lastIndex)
                        
                        if(insertIndex % 2 === 0 ) {
                            injectAd('A', 99 + index, index)
                        } else {
                            injectAd('B', 100 + index, index)
                        }
                    }
                });
            } 
            // Desktop
            else {
                function useSkyscraper(version, number, index) {
                    $('.sidebar').children('.o-advertisement--box').addClass('o-advertisement--skyscraper').removeClass('o-advertisement--box')
                }

                function stickyAds(scrollTop, windowHeight, headerHeight, sidebarOffset, stickyElements, scrollDistance) {
                    
                    // console.log(scrollTop, stickyElements[0].offset)
                    
                    stickyElements.map(stickyElement => {
                        // console.log(scrollTop, stickyElement.offset)
                        const stickyElementHeight = $(stickyElement.element).height()
        
                        const dropoff = stickyElement.offset + scrollDistance*windowHeight - stickyElementHeight - sidebarOffset
                        const pickup = scrollTop + headerHeight + sidebarOffset
        
                        // Dropoff bottom
                        if (scrollTop > dropoff) {
                            if (!stickyElement.dropoff) {
                                stickyElement.dropoff = dropoff
                            }
        
                            const topOffset = String( dropoff - stickyElementHeight - headerHeight) + 'px'
                            stickyElement.element.css('position', 'absolute')
                            stickyElement.element.css('margin-top', topOffset)
                        } 
                        // Pickup
                        else if (pickup > stickyElement.offset) {
                            if (!stickyElement.pickup) {
                                stickyElement.pickup = pickup
                            }
                            
                            const topOffset = String(headerHeight + sidebarOffset) + 'px'
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

                useSkyscraper();

                $( window ).on( "load", function() {
                    // Setup sticky ads
                    const headerHeight = $('.topbar').height();
                    const sidebarOffset = parseInt($('.sidebar.offset').css('margin-top'), 10)
                    let stickyElements = []
                    const scrollDistance = 1.5
            
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

                        stickyAds(scrollTop, windowHeight, headerHeight, sidebarOffset, stickyElements, scrollDistance)
                    })

                    // Inline Ads
                    // First inline ad should be after dropoff of sticky
                    let insertIndex = Math.floor((Math.random() * 3) + 3);
                    let lastIndex = null
                    $(paragraphs).each(function(index) {
                        
                        if(index === insertIndex) {
                            lastIndex = insertIndex
                            insertIndex += Math.floor((Math.random() * 3) + 3);
                            console.log(insertIndex, lastIndex)
                            
                            // let lastIndex = adOffsets[adOffsets.indexOf(index) - 1]
                            if(insertIndex % 2 === 0 ) {
                                injectAd('A', 99 + index, index)
                            } else {
                                injectAd('B', 100 + index, index)
                            }
                        }
                    });
                })
            }
        })
    }
    
    injectInlineAds()
    
    var articleList = React.render(
        <ArticleList breakpoint={960} name={listName} firstArticle={firstArticle} articles={articleIds} userId={userId} />,
        document.getElementById('article-list')
    );
}

React.render(
    <Search />,
    document.getElementById('search-form')
);

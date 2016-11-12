var Galleries = require('./Galleries.jsx');
var mp = require('../modules/Mixpanel');

var Article = React.createClass({

    getInitialState: function(){
        return {
            galleries: [],
        }
    },

    componentDidMount: function(){
        // Setup galleries after DOM is loaded
        this.setState({ galleries: this.setupGalleries() });
        this.injectInlineAds();
        this.addTrackingEventListeners();
        this.executeAJAXLoadedScripts();

        window.fbRefresh();
        window.twttrRefresh();

        this.isViewed = false;
    },

    componentDidUpdate(prevProps, prevState) {
      if (this.props.isActive && !prevProps.isActive) {
        this.injectInlineAds();
        this.trackEvents();

        if (this.props.index > 0) {
          window.resetAds('#article-' + this.props.articleId);
        } else {
          window.resetAds(document);
        }
      }
    },

    trackEvents() {
      if (this.props.index > 0 && !this.isViewed) {
        mp.pageView(
          'article',
          $('#article-' + this.props.articleId + ' > article'),
          this.props.index + 1
        );
        this.isViewed = true;
      }
    },

    addTrackingEventListeners() {
      var $article = $('#article-' + this.props.articleId + ' > article');

      $article.on('click', 'a.facebook', function() {
        mp.shareArticle('facebook', $article);
      });

      $article.on('click', 'a.twitter', function() {
        mp.shareArticle('twitter', $article);
      });
    },

    injectInlineAds() {
      // If on mobile, insert box advertisement after 2nd and 7th paragraphs
      if ($(window).width() < 960) {
        var paragraphs = $('#article-' + this.props.articleId + ' .article-content > p');

        var articleId = this.props.articleId;

        function injectAd(version, number, index) {
          var id = 'div-gpt-ad-1443288719995-' + number + '-' + articleId;
          var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement o-advertisement--box o-advertisement--center"><div class="adslot" id="' + id + '" data-size="box" data-dfp="Box_' + version + '_300x250"></div></div></div></div>';

          if (!$('#' + id).length) {
            $(adString).insertAfter(paragraphs.get(index));
          }
        }

        if (paragraphs.length > 2) {
          injectAd('A', 99, 1);
        }

        if (paragraphs.length > 8 ) {
          injectAd('B', 100, 6);
        }
      }
    },

    executeAJAXLoadedScripts: function() {
        var scripts = $("#article-list").find("script");
        for (var i=0;i<scripts.length;i++) {
          if(!scripts[i].src) {
            eval(scripts[i].innerHTML);
          }
        }
    },

    setupGalleries: function(){

        var gatherImages = function(gallery){

            var selector, trigger;

            if(gallery){
                var id = $(gallery).data("id");
                selector = '#gallery-' + id + ' .gallery-image';
                trigger = '#gallery-' + id + ' .gallery-thumb';
            } else {
                selector = '#article-' + this.props.articleId + ' .article-attachment';
                trigger = '#article-' + this.props.articleId + ' .article-attachment';
            }

            var images = [];
            var imagesTable = {};
            var n = 0;

            $(selector).each(function(){
                var id = $(this).data('id');
                images.push({
                    'id': id,
                    'url': $(this).data('url'),
                    'caption': $(this).data('caption'),
                    'credit': $(this).data('credit'),
                    'width': $(this).width(),
                    'height': $(this).height()
                });
                imagesTable[id] = n;
                n++;
            });

            return {
                'title': gallery ? $(gallery).data("id") : "Images",
                'list': images,
                'table': imagesTable,
                'selector': selector,
                'trigger': trigger
            }

        }.bind(this);

        var galleries = [];

        galleries.push(gatherImages());

        $('#article-'+this.props.articleId+ ' .gallery-attachment').each(function(){
            galleries.push(gatherImages(this));
        });

        return galleries;

    },

    renderHTML: function(){
        var html = {'__html': this.props.html};
        return (<div ref="article"  className="article-html" dangerouslySetInnerHTML={html}></div>);
    },

    render: function(){
        var html = {'__html': this.props.html};
        return (
            <div className={this.props.html ? "article-slide" : "article-extras"}>
                {this.props.html ? this.renderHTML() : null}
                <Galleries galleries={this.state.galleries} />
            </div>
            );
    }
});

module.exports = Article;

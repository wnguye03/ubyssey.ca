import React from 'react';
import Galleries from './Galleries.jsx';
import * as mp from '../modules/Mixpanel';

const Article = React.createClass({

    getInitialState() {
      return {
        galleries: [],
      }
    },

    componentDidMount() {
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
          window.resetAds(`#article-${this.props.articleId}`);
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
      const $article = $(`#article-${this.props.articleId} > article`);

      $article.on('click', 'a.facebook', () => {
        mp.shareArticle('facebook', $article);
      });

      $article.on('click', 'a.twitter', () => {
        mp.shareArticle('twitter', $article);
      });
    },

    injectInlineAds() {
      // If on mobile, insert box advertisement after 2nd and 7th paragraphs
      if ($(window).width() < 960) {
        const paragraphs = $(`#article-${this.props.articleId} .article-content > p`);

        var articleId = this.props.articleId;

        function injectAd(version, number, index) {
          const id = `div-gpt-ad-1443288719995-${number}-${articleId}`;
          var adString = '<div class="o-article-embed o-article-embed--advertisement"><div class="o-article-embed__advertisement"><div class="o-advertisement o-advertisement--box o-advertisement--center"><div class="adslot" id="' + id + '" data-size="box" data-dfp="Box_' + version + '"></div></div></div></div>';

          if (!$(`#${id}`).length) {
            $(adString).insertAfter(paragraphs.get(index));
          }
        }

        if (paragraphs.length > 2) {
          injectAd('A', 99, 1);
        }

        if (paragraphs.length > 8) {
          injectAd('B', 100, 6);
        }
      }
    },

    executeAJAXLoadedScripts() {
        var scripts = $("#article-list").find("script");
        for (var i=0;i<scripts.length;i++) {
          if(!scripts[i].src) {
            eval(scripts[i].innerHTML);
          }
        }
    },

    setupGalleries() {

        const gatherImages = function(gallery) {
          var selector, trigger;

          if (gallery) {
            const id = $(gallery).data("id");
            selector = `#gallery-${id} .gallery-image`;
            trigger = `#gallery-${id} .gallery-thumb`;
          } else {
            selector = `#article-${this.props.articleId} .article-attachment`;
            trigger = `#article-${this.props.articleId} .article-attachment`;
          }

          const images = $(selector).map((_, el) => {
            const $el = $(el);
            return {
              id: $el.data('id'),
              url: $el.data('url'),
              caption: $el.data('caption'),
              credit: $el.data('credit'),
              width: $el.width(),
              height: $el.height()
            };
          }).get();

          const imagesTable = images.reduce((table, image, i) => {
            table[image.id] = i;
            return table;
          }, {});

          return {
            selector,
            trigger,
            title: gallery ? $(gallery).data('id') : 'Images',
            list: images,
            table: imagesTable,
          };
        }.bind(this);

        return [
          gatherImages(),
          ...$(`#article-${this.props.articleId} .gallery-attachment`)
            .map((_, elem) => gatherImages(elem)).get()
        ];
    },

    renderHTML() {
      const html = {__html: this.props.html};
      return (<div ref="article"  className="article-html" dangerouslySetInnerHTML={html}></div>);
    },

    render() {
      const html = {__html: this.props.html};
      return (
          <div className={this.props.html ? "article-slide" : "article-extras"}>
              {this.props.html ? this.renderHTML() : null}
              <Galleries galleries={this.state.galleries} />
          </div>
          );
    }
});

export default Article;

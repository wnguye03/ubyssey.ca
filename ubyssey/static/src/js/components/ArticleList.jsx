import React from 'react';
import Article from './Article.jsx';
var CommentsBar = require('./CommentsBar.jsx');
import ArticleHeader from './ArticleHeader.jsx';
import LinkedList from '../modules/LinkedList';

const ArticleList = React.createClass({
    getInitialState() {
        var articles = this.props.articles;
        articles.unshift(this.props.firstArticle.id);

        return {
            active: new LinkedList(articles),
            articles: [this.props.firstArticle],
            loading: false,
        }
    },
    componentWillMount() {
        this.articlesTable = {};
        this.articlesTable[this.props.firstArticle.id] = 0;
    },
    componentDidMount() {
        this.loaded = [this.props.firstArticle.id];
        this.afterLoad = null;

        this.scrollListener();
        if(this.state.active.next)
            this.loadNext(this.state.active.next.data);
    },
    adjustHeaderForBanner() {
      const bannerHeight= $('.c-banner').outerHeight();
      if (bannerHeight) {
        $('.header-article').css('top', bannerHeight);
      }
    },
    updateHeader(topPos) {
        if (topPos > 50 && !window.articleHeader){
            window.articleHeader = true;
            $('.header-site').css('visibility', 'hidden');
            $('.header-article').show();
        } else if (topPos < 50 && window.articleHeader){
            window.articleHeader = false;
            $('.header-article').hide();
            // Only display site header if width > $bp-larger-than-tablet
            if($(window).width() > 960) {
              $('.header-site').css('visibility', 'visible');
            }
        }
        this.adjustHeaderForBanner();
    },
    getArticle(id) {
        return this.state.articles[this.articlesTable[id]];
    },
    getArticlePoints() {
        const $article = $(`#article-${this.state.active.data}`);
        const height = $article.height();
        const top = $article.position().top;
        const end = top + height;
        return {
            top,
            mid: Math.round(end - (height / 2)),
            end,
            height
        }
    },
    scrollListener() {
        const windowHeight = $(window).height();
        const documentHeight = $(document).height();

        var cachedPoints;
        var points;

        var updateScroll = () => {
            const topPos = $('#content-wrapper').scrollTop();
            const bottomPos = topPos + windowHeight;

            if($(window).width() > 960)
                this.updateHeader(topPos);

            if(cachedPoints != this.state.active.data){
                points = this.getArticlePoints();
                cachedPoints = this.state.active.data;
            }

            if(bottomPos > points.end)
                this.prepNext();

            if(topPos > points.end - ((windowHeight / 2) - 50) || (points.height < windowHeight && bottomPos > (documentHeight - 50)))
                this.setNext();

            if(bottomPos < points.top - 50)
                this.setPrev();
        };

        $('#content-wrapper').scroll(updateScroll);

    },
    prepNext() {
        if(!this.state.active.next || !this.state.active.next.next) {
          return;
        }

        if(!this.isLoaded(this.state.active.next.next.data)) {
          this.loadNext(this.state.active.next.next.data);
        }
    },
    setNext() {
        if(!this.state.active.next)
            return;

        if(!this.isLoaded(this.state.active.next.data)){
            this.loadNext(this.state.active.next.data);
            this.afterLoad = this.setNext;
            return;
        }

        if(this.state.loading){
            this.afterLoad = this.setNext;
            return;
        }

        // Google Analytics pageview
        ga('send', 'pageview');

        this.setState({ active: this.state.active.next }, () => this.updateURL());
    },
    setPrev() {
        if(!this.state.active.prev)
            return;

        this.setState({ active: this.state.active.prev }, () => this.updateURL());
    },
    updateURL() {
        try {
            history.replaceState(
                history.state, 
                this.getArticle(this.state.active.data).headline, 
                this.getArticle(this.state.active.data).url
            );
        } catch(err) {}
    },
    loadNext(articleId) {
        if (this.state.loading || this.isLoaded(articleId))
            return;
        this.loadArticle(articleId);
    },
    isLoaded(id) {
        return this.loaded.indexOf(parseInt(id)) !== -1;
    },
    loadArticle(articleId) {
        this.setState({ loading: true });
        dispatch.articleRendered(articleId, data => {
            this.loaded.push(parseInt(articleId));
            this.renderArticle(data);
        });
    },
    renderArticle(data) {
        const articles = [...this.state.articles, data];

        this.articlesTable[data.id] = articles.length - 1;

        this.setState({ loading: false, articles }, () => {
            if (this.afterLoad) {
              this.afterLoad();
            }
            this.afterLoad = null;
        });
    },
    render() {
        const articles = this.state.articles.map((article, i) => (
            <Article isActive={this.state.active.data==article.id} articleId={article.id} html={article.html} key={article.id} index={i} />
        ));

        return (
            <div>
                <ArticleHeader name={this.props.name} headline={this.getArticle(this.state.active.data).headline} />
                {articles}
            </div>
        );
    }
})

export default ArticleList;

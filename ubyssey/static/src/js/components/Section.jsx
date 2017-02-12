import React from 'react';
import {formatPubDate} from '../modules/Dates';

const Section = React.createClass({
    getInitialState() {
        return {
            articles: [],
            loading: false,
        }
    },
    componentDidMount() {
        this.loaded = 0;
        this.scrollListener();
    },
    scrollListener() {
        $(window).scroll(() => {
            const windowHeight = $(window).height();
            const documentHeight = $(document).height();
            const topPos = $(document).scrollTop();
            const bottomPos = topPos + windowHeight;

            if(bottomPos == documentHeight)
                this.loadMore();
        });
    },
    renderSpinner() {
        return (
            <div className="spinner">
              <div className="rect1"></div>
              <div className="rect2"></div>
              <div className="rect3"></div>
              <div className="rect4"></div>
              <div className="rect5"></div>
            </div>
            );
    },
    loadMore() {
        if(this.state.loading || this.loaded >= 5)
            return;

        this.setState({ loading: true });

        var query = { offset: 7 + (6 * this.loaded), limit: 6 }
        query[this.props.type] = this.props.id;

        dispatch.search('article', query, data => {
            this.loaded++;
            this.setState({ articles: this.state.articles.concat(data.results), loading: false });
        });
    },
    renderImage(article) {
        const style = { backgroundImage: `url('${article.featured_image.url}')` };
        return (
            <a href={article.url} className="image image-aspect-4-3">
                <div style={style}></div>
            </a>
            )
    },
    render() {
        const articles = this.state.articles.map((article, i) => (
            <article key={i}>
                {article.featured_image && this.renderImage(article)}
                <a href={ article.url }>
                    <h2 className="headline" dangerouslySetInnerHTML={{__html: article.headline}}></h2>
                </a>
                <span className="byline">
                    <span className="author">By { article.authors_string }</span> &nbsp;·&nbsp; <span className="published">{ formatPubDate(article.published_at) }</span>
                </span>
                <p className="snippet">{ article.snippet }</p>
            </article>
        ));

        return (
            <div>
                <div className="blocks">{articles}</div>
                {this.state.loading && this.renderSpinner()}
            </div>
        )
    }
});

export default Section;

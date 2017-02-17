import React from 'react';
import LRU from 'lru-cache';

const Search = React.createClass({
    getDefaultProps() {
        return {
            cacheOptions: {
                max: 150,
            },
        }
    },
    getInitialState() {
        return {
            results: [],
            cache: LRU(this.props.cacheOptions),  // entries are {q: results}
            q: '',
            prevQ: '',
        }
    },
    componentDidMount() {
        this.refs.search.getDOMNode().focus();
    },
    updateQuery(event) {
        this.setState({
            prevQ: this.state.q,
            q: event.target.value
        }, this.search);
    },
    search() {
        const q = this.state.q;
        if (q.length > 0){
            if (q.length > 1 && q.length > this.state.prevQ.length && this.state.results.length == 0) {
                // We've already typed one char and got no results, so
                // adding more chars to query (making it more specific) cannot help.
                return;
            }

            if (this.state.cache.has(q)) {
                this.setState({ results: this.state.cache.get(q) });
            } else {
                dispatch.search('article', { q }, data => {
                    this.setState(prevState => {
                        prevState.results = data.results;
                        prevState.cache.set(q, data.results);
                        return prevState;
                    });
                });
            }
        } else {
            this.setState({ results: [] });
        }
    },
    render() {
        const results = this.state.results.map((item, i) => (
            <li key={i}><a href={item.url}>{item.headline}</a></li>
        ));

        return (
            <div className="u-container">
                <form method="get" action="/archive/">
                    <label htmlFor="author-search"><i className="fa fa-search"></i></label>
                    <input ref="search" className={this.state.results.length > 0 ? "open" : ""} name="q" id="search-bar" type="text" autoComplete="off" onChange={this.updateQuery} value={this.state.q} placeholder="Search The Ubyssey..." />
                </form>
                <ul className={"results" + (this.state.results.length > 0 ? " open" : "")}>{results}</ul>
            </div>
        )
    }
});

export default Search;

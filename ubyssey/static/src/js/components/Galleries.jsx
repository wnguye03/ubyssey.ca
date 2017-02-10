import React from 'react';
import Gallery from './Gallery.jsx';

const Galleries = React.createClass({
    render() {
        const galleries = this.props.galleries.map(function(gallery, i){
            return (<Gallery key={i} title={gallery.title} trigger={gallery.trigger} selector={gallery.selector} images={gallery.list} imagesTable={gallery.table} />);
        });
        return (<div>{galleries}</div>);
    }
});

export default Galleries;

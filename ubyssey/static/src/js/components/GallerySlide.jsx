import React from 'react';

const GallerySlide = React.createClass({
  render() {
    const slideStyle = { width: this.props.width };
    const imageStyle = { backgroundImage: `url('${this.props.src}')` };

    return (
      <li className="slide" style={slideStyle}>
        <div className="inner">
          <div className="image">
            <div>
              <div className="img" style={imageStyle}></div>
            </div>
          </div>
          <div className='slide-meta'>
            { this.props.caption &&
              <p className="slide-caption" dangerouslySetInnerHTML={{__html: this.props.caption}}></p> }
            { this.props.credit &&
              <p className="slide-credit" dangerouslySetInnerHTML={{__html: this.props.credit}}></p> }
          </div>
        </div>
      </li>
    );
  }
});

export default GallerySlide;

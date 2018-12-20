import React from 'react'
import ArticleBox from './ArticleBox.jsx'

class Magazine extends React.Component{
  constructor(props) {
    super(props)
    this.subsections = Object.keys(this.props)
    this.state = {
      subsection: 'Reclaim'
    }
  }

  render() {
    return (
      <div className="magazine-container">
        <div >
          {
            this.state.subsection !== null && 
            <div className="article-grid-container" >
              {this.props[this.state.subsection].map((box, index) => {
                return(
                  <ArticleBox color={box.color}
                    index={index}
                    subsection={this.state.subsection}
                    url={box.url}
                    image={box.featured_image}
                    headline={box.headline}/>
                )
              })}
            </div>
          }
        </div>

      </div>
    )
  }
}

export default Magazine
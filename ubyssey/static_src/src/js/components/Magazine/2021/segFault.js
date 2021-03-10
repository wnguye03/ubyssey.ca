import React, { Component } from 'react'

export default class segFault extends Component {
    render() {
        return (
            <div>

                <div className="wrapper">

                    <div className="grid_container fade-in">
                        {this.props.articles.map((article, index) => {

                            return (

                                <div className={`article_${index} nested one`}>

                                    <div>
                                        <img className="photo_vertical" src={article.featured_image} />

                                    </div>
                                    <div> <h2 style={{ color: 'white' }}>{article.headline}</h2></div>
                                    <div className="card__overlay"> <a href={article.url}> <span> Read More </span></a> </div>
                                </div>
                            )



                        })}

                    </div>

                </div>


            </div>
        )
    }
}

import React from "react"
import ReactDOM from "react-dom"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  ReactDOM.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
      waysForwardImage={$("#magazine-wrapper").data("waysforward-image")}
      comesAroundImage={$("#magazine-wrapper").data("comesaround-image")}
      goesAroundImage={$("#magazine-wrapper").data("goesaround-image")}
      title={$("#magazine-wrapper").data("title")}
    />,
    $("#magazine-wrapper")[0]
  )
})

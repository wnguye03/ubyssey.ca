import React from "react"
import ReactDOM from "react-dom"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  ReactDOM.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
      waysForwardImage={$("#magazine-wrapper").data("waysForwardImage")}
      comesAroundImage={$("#magazine-wrapper").data("comesAroundImage")}
      goesAroundImage={$("#magazine-wrapper").data("goesAroundImage")}
      title={$("#magazine-wrapper").data("title")}
    />,
    $("#magazine-wrapper")[0]
  )
})

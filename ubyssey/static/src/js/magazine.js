import React from "react"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  React.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
      insideCover={$("#magazine-wrapper").data("insideCover")}
      title={$("#magazine-wrapper").data("title")}
    />,
    $("#magazine-wrapper")[0]
  )
})

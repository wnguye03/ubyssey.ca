/** @format */

import React from "react"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  React.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
    />,
    $("#magazine-wrapper")[0]
  )
})

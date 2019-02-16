import React from "react"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  React.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
      resolveImage={$("#magazine-wrapper").data("resolveImage")}
      redefineImage={$("#magazine-wrapper").data("redefineImage")}
      reclaimImage={$("#magazine-wrapper").data("reclaimImage")}
      title={$("#magazine-wrapper").data("title")}
    />,
    $("#magazine-wrapper")[0]
  )
})

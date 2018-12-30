/** @format */

import React from "react"
import { Magazine } from "./components/Magazine/2019"

$(function() {
  React.render(
    <Magazine
      articles={$("#magazine-wrapper").data("articles")}
      cover={$("#magazine-wrapper").data("cover")}
      title={$("#magazine-wrapper").data("title")}
    />,
    $("#magazine-wrapper")[0]
  )
})

// const grids = {
//   reclaim: [33.3, 66.7, 66.7, 33.3, 100],
//   redefine: [33.3, 66.7, 66.7, 33.3, 100],
//   resolve: [33.3, 66.7, 66.7, 33.3, 100],
// }

// const time1 = 250

// function removeCover() {
//   $("#magazine-cover").animate({ opacity: 0 }, time1, function() {
//     $(this).hide()
//     addGrid()
//   })
// }

// function addCover() {
//   $("#magazine-cover")
//     .show()
//     .animate({ opacity: 1 }, time1)
// }

// function removeGrid() {
//   if (window.currentView === "cover") {
//     $("#magazine-header").fadeOut(time1)
//   }
//   $(`.article-grid.${window.lastView}`).each(function(index) {
//     $(this)
//       .delay((index * time1) / 2)
//       .animate({ opacity: 0 }, time1, function() {
//         if (index >= $(`.article-grid.${window.lastView}`).length - 1) {
//           $(`.article-grid.${window.lastView}`).hide()
//           $("#magazine-article-grid").hide()
//           console.log(window.currentView)
//           if (window.currentView === "cover") {
//             addCover()
//           } else {
//             addGrid()
//           }
//         }
//       })
//   })
// }

// function addGrid() {
//   $("#magazine-header")
//     .fadeIn(3 * time1)
//     .css("display", "flex")
//   // .animate({ opacity: 1 }, time1)
//   $("#magazine-article-grid").css("display", "flex")

//   $(`.article-grid.${window.currentView}`).css("display", "block")

//   $(`.article-grid.${window.currentView}`).each(function(index) {
//     $(this)
//       .css("flex-basis", `${grids[window.currentView][index]}%`)
//       .delay((index * time1) / 2)
//       .animate({ opacity: 1 }, time1, function() {
//         $(this).addClass("hover")
//       })
//   })
// }

// $(function() {
//   $(".c-cover__option").on("click touch", function() {
//     window.lastView = "cover"
//     if ($(this).hasClass("reclaim")) {
//       window.currentView = "reclaim"
//     } else if ($(this).hasClass("resolve")) {
//       window.currentView = "resolve"
//     } else if ($(this).hasClass("redefine")) {
//       window.currentView = "redefine"
//     }
//     removeCover()
//   })

//   $(".subsection").on("click touch", function() {
//     $("#magazine-cover").hide()
//     window.lastView = window.currentView
//     if ($(this).hasClass("reclaim")) {
//       window.currentView = "reclaim"
//     } else if ($(this).hasClass("resolve")) {
//       window.currentView = "resolve"
//     } else if ($(this).hasClass("redefine")) {
//       window.currentView = "redefine"
//     } else if ($(this).hasClass("cover")) {
//       window.currentView = "cover"
//     }
//     removeGrid()
//   })
// })

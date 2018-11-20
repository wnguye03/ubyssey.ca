import React from 'react'
import { FoodInsecurity } from './components/FoodInsecurity'

$(function () {
  $('.food-insecurity').each(function() {
      React.render(
          <FoodInsecurity  id={$(this).data('currentArticleId')}
                      map={$(this).data('map')} 
                      pointData={$(this).data('pointData')} />,
          $(this).get(0)
      )
  })
});

import React from 'react'
import { Magazine } from './components/Magazine/2019'

$(function () {
  React.render(
    <Magazine  
      Reclaim={$('#magazine-wrapper').data('articlesReclaim')}
      Resolve={$('#magazine-wrapper').data('articlesResolve')}
      Redefine={$('#magazine-wrapper').data('articlesRedefine')}
      />,
    $('#magazine-wrapper')[0]
  )
});


import React from 'react'
import { Magazine } from './components/Magazine/2019'

$(function () {
  React.render(
    <Magazine  temp={$('#magazine-wrapper').data('temp')}/>,
    $('#magazine-wrapper')[0]
  )
});


function normalize(current, min, max) {
  return (current - max) / (min - max)
}

function lint(current, min, max, start, end) {
  return min + (max-min) * normalize(current, start, end);
}


export function timelineHeight() {
  const startHeight = window.innerHeight/2
  const endHeight = window.innerHeight/4

  $(document).ready(function () {
    console.log($(window).width())
    $('.timeline-container').width($(window).width()-17)
    $('#content-wrapper').scroll(() => {
      const scrollTop = $('#content-wrapper').scrollTop();
      if (scrollTop < endHeight) {
        $('.timeline-container').height(startHeight - scrollTop)
        $('.timeline-container > h1').css('right', String((lint(startHeight - scrollTop, 450, 0, startHeight, endHeight)) + 'px'))
        $('.timeline-container > h1').css('bottom', String((lint(startHeight - scrollTop, -20, 100, startHeight, endHeight)) + 'px'))
        $('.timeline-container > h1').css('font-size', String((lint(startHeight - scrollTop, 32, 60, startHeight, endHeight)) + 'px'))
        $('.timeline-tree').css('width', String((lint(startHeight - scrollTop, 60, 75, startHeight, endHeight)) + '%'))
        $('.timeline-tree').css('margin-left', String((lint(startHeight - scrollTop, 15, 0, startHeight, endHeight)) + '%'))
        // $('.c-timeline').css('position', 'static')
      } else if (scrollTop >= endHeight) {
        $('.timeline-container').height(startHeight - scrollTop)
        $('.timeline-container > h1').css('right', String(450) + 'px')
        $('.timeline-container > h1').css('bottom', String(20) + 'px')
        $('.timeline-container > h1').css('font-size', String(32) + 'px')
        $('.timeline-tree').css('width', String(60) + '%')
        $('.timeline-tree').css('margin-left', String(15) + '%')
      }
    })
  })
}


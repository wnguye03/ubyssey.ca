export function timelineHeight() {
  $(document).ready(function () {
    $('#content-wrapper').scroll(() => {
      const scrollTop = $('#content-wrapper').scrollTop();
      if (scrollTop < window.innerHeight/4) {
        $('.timeline-container').height(window.innerHeight/2 - scrollTop)
        console.log(scrollTop, window.innerHeight/2 - scrollTop)
      } 
    })
  })
}


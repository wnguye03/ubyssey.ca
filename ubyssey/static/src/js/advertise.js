$(function() {

  // Navigation links smooth scrolling
  $('a[href*=\\#]').on('click', function(event){
    console.log(event);
    event.preventDefault();
    $('html,body').animate({scrollTop:$(this.hash).offset().top}, 500);
  });

  $('.o-placements--web .o-placements__placement').click(function() {
    $('.o-placements--web .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements--web .o-placements__demo__inner img').css('top', $(this).data('offset'));
  });

  $('.o-placements--print .o-placements__placement').click(function() {
    $('.o-placements--print .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');

    $('.o-placements--print .o-placements__demo').attr('data-demo', $(this).data('demo'));
  });

  // Open modal
  $('.c-production-schedule__view').click(function() {
    $('.c-production-schedule__modal').show();
  })

  // Close modal
  $('.c-production-schedule__modal__close').click(function() {
    $('.c-production-schedule__modal').hide();
  });

  $('.c-production-schedule__modal').click(function() {
    $('.c-production-schedule__modal').hide();
  });

  $('.c-production-schedule__modal img').click(function(e) {
    e.stopPropagation()
  });

});

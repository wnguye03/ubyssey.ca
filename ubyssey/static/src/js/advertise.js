$(function() {

  $('.o-placements--web .o-placements__placement').click(function() {
    console.log('click');
    $('.o-placements--web .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements--web .o-placements__demo__inner img').css('top', $(this).data('offset'));
  });

});

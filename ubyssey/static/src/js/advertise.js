$(function() {

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

});

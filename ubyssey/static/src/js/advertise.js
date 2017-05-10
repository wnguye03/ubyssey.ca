$(function() {
  $('.o-placements__placement').click(function() {
    $('.o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements__demo').attr('data-demo', $(this).data('demo'));
  });
});

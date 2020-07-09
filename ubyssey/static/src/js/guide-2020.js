const colors = {
  colorHome: "#0073A9",
  colorAdulting: "#59A3AC",
  colorAcademics: "#FBCC80",
  colorSDP: "#E2BEB0",
  colorVancouver: "#EA8392",
  colorUBC: "#002145"
}

window.onload = function() {
  if (window.location.href.indexOf("academics") > -1) {
    $('#c-header').css('background-color', colors.colorAcademics);
    $('.c-footer').css('background-color', colors.colorAcademics);
    document.getElementById("section-academics").style.display = 'block';
   } else if (window.location.href.indexOf("adulting") > -1) {
    $('#c-header').css('background-color', colors.colorAdulting);
    $('.c-footer').css('background-color', colors.colorAdulting);
    document.getElementById("section-adulting").style.display = 'block';
   } else if (window.location.href.indexOf("sdp") > -1) {
     $('#c-header').css('background-color', colors.colorSDP);
     $('.c-footer').css('background-color', colors.colorSDP);
     document.getElementById("section-sdp").style.display = 'block';
   } else if (window.location.href.indexOf("vancouver") > -1) {
     $('#c-header').css('background-color', colors.colorVancouver);
     $('.c-footer').css('background-color', colors.colorVancouver);
     document.getElementById("section-vancouver").style.display = 'block';
   } else if (window.location.href.indexOf("ubc") > -1) {
    $('#c-header').css('background-color', colors.colorUBC);
    $('.c-footer').css('background-color', colors.colorUBC);
    document.getElementById("section-ubc").style.display = 'block';
   } else {
     $('#c-header').css('background-color', colors.colorHome);
     $('.c-footer').css('background-color', colors.colorHome);
     document.getElementById("section-academics").style.display = 'block';
     document.getElementById("section-adulting").style.display = 'block';
     document.getElementById("section-sdp").style.display = 'block';
     document.getElementById("section-vancouver").style.display = 'block';
     document.getElementById("section-ubc").style.display = 'block';
   }
}

$(document).ready(function(){
  $('#c-nav-home').hover(function(e) {
    e.stopPropagation();
    $('.c-home-more').finish();
    $('.c-home-more').slideToggle(300);
    }, (function(e) {
      e.stopPropagation();
      $('.c-home-more').finish();
      $('.c-home-more').fadeOut(300);
    })
  );
 });
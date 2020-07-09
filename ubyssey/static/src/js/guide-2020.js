const colors = {
  colorHome: "#0073A9",
  colorAdulting: "#59A3AC",
  colorAcademics: "#FBCC80",
  colorSDP: "#E2BEB0",
  colorVancouver: "#EA8392",
  colorUBC: "#002145"
}

$(document).ready(function(){
  if (window.location.href.indexOf("academics") > -1) {
    $('#c-header').css('background-color', colors.colorAcademics);
    $('#c-footer').css('background-color', colors.colorAcademics);
    if(document.getElementById("section-academics") != null) {
      document.getElementById("section-academics").style.display = 'block';
    }
   } else if (window.location.href.indexOf("adulting") > -1) {
    $('#c-header').css('background-color', colors.colorAdulting);
    $('#c-footer').css('background-color', colors.colorAdulting);
    if(document.getElementById("section-adulting") != null) {
      document.getElementById("section-adulting").style.display = 'block';
    }
   } else if (window.location.href.indexOf("sdp") > -1) {
     $('#c-header').css('background-color', colors.colorSDP);
     $('#c-footer').css('background-color', colors.colorSDP);
     if(document.getElementById("section-sdp") != null) {
      document.getElementById("section-sdp").style.display = 'block';
     }
   } else if (window.location.href.indexOf("vancouver") > -1) {
     $('#c-header').css('background-color', colors.colorVancouver);
     $('#c-footer').css('background-color', colors.colorVancouver);
     if(document.getElementById("section-vancouver") != null) {
      document.getElementById("section-vancouver").style.display = 'block';
     }
   } else if (window.location.href.indexOf("ubc") > -1) {
    $('#c-header').css('background-color', colors.colorUBC);
    $('#c-footer').css('background-color', colors.colorUBC);
    if(document.getElementById("section-ubc") != null) {
      document.getElementById("section-ubc").style.display = 'block';
    }
   } else {
     $('#c-header').css('background-color', colors.colorHome);
     $('#c-footer').css('background-color', colors.colorHome);
     if(document.getElementById("section-academics") != null) {
      document.getElementById("section-academics").style.display = 'block';
     }
     if(document.getElementById("section-adulting") != null) {
      document.getElementById("section-adulting").style.display = 'block';
     }
     if(document.getElementById("section-ubc") != null) {
      document.getElementById("section-ubc").style.display = 'block';
     }
     if(document.getElementById("section-vancouver") != null) {
      document.getElementById("section-vancouver").style.display = 'block';
     }
     if(document.getElementById("section-sdp") != null) {
      document.getElementById("section-sdp").style.display = 'block';
     }
   }

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

window.onload = function() {
  document.getElementById("c-header").style.display = 'block';
  document.getElementById("c-footer").style.display = 'flex';
}
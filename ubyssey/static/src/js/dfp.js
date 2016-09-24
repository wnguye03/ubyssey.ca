var sizes = {
    'box': [300, 250],
    'leaderboard': [728, 90],
    'mobile-leaderboard': [300, 50]
};

var googletag = googletag || {};
googletag.cmd = googletag.cmd || [];

window.googletag = googletag;

function DFP(element) {

  var self = this;

  // Set default values
  self.adslots = [];
  self.element = document;

  // Inject GPT script tag into document
  (function() {
    var gads = document.getElementById('gpt-script') || document.createElement('script');
    gads.id = 'gpt-script';
    gads.async = true;
    gads.type = 'text/javascript';
    var useSSL = 'https:' == document.location.protocol;
    gads.src = (useSSL ? 'https:' : 'http:') + '//www.googletagservices.com/tag/js/gpt.js';
    var node = document.getElementsByTagName('script')[0];
    node.parentNode.insertBefore(gads, node);
  })();

  function setup() {
    // Infinite scroll requires SRA
    googletag.pubads().enableSingleRequest();

    // Disable initial load, we will use refresh() to fetch ads.
    // Calling this function means that display() calls just
    // register the slot as ready, but do not fetch ads for it.
    googletag.pubads().disableInitialLoad();

    // Enable services
    googletag.enableServices();
  }

  function collectAds() {
    var dfpslots = $(self.element).find(".adslot").filter(":visible");

    googletag.destroySlots();

    $(dfpslots).each(function(){
      var slotName = $(this).attr('id'),
          slot = googletag.defineSlot('/61222807/'+$(this).data('dfp'), sizes[$(this).data('size')], slotName);

      self.adslots.push([
        slotName,
        slot.addService(googletag.pubads())
      ]);
    });
  }

  function refreshAds() {
    $.each(self.adslots, function(i, slot) {
      googletag.display(slot[0]);
      googletag.pubads().refresh([slot[1]]);
    });
  };

  return {
    load: function(element) {
      self.element = element;
      googletag.cmd.push(setup);
      googletag.cmd.push(collectAds);
      googletag.cmd.push(refreshAds);
    },
    reset: function() {
      self.adslots = [];
      googletag.cmd.push(googletag.destroySlots);
    }
  }
}

var dfp = DFP();

$(document).ready(function() {
  dfp.load(document);
});

window.resetAds = function(element) {
  dfp.reset();
  dfp.load(element);
}

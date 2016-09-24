var SIZES = {
    'box': [300, 250],
    'leaderboard': [728, 90],
    'mobile-leaderboard': [300, 50]
};

// Get reference to googletag from window object
googletag = window.googletag;

function DFP(element) {

  var self = this;

  // Set default values
  self.adslots = [];
  self.element = document;

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
          slot = googletag.defineSlot('/61222807/'+$(this).data('dfp'), SIZES[$(this).data('size')], slotName);

      slot.setCollapseEmptyDiv(true);

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

(function() {
  // ---- Page Registration ----
  // Add page IDs here (without "page-" prefix).
  // Must match the .page#page-[name] in your .pug files.
  var publicPages = ['home', 'login'];
  var loggedPages = ['dashboard'];
  var allPages = publicPages.concat(loggedPages);

  function navigate() {
    var hash = location.hash.replace('#','') || 'home';
    if (allPages.indexOf(hash) === -1) hash = 'home';

    // Hide all pages, show target
    document.querySelectorAll('.page').forEach(function(p) {
      p.classList.remove('active');
    });
    var target = document.getElementById('page-' + hash);
    if (target) target.classList.add('active');

    // Update sidebar active state
    document.querySelectorAll('.sidebar nav a').forEach(function(a) {
      var linkHash = a.getAttribute('href').replace('#','');
      a.classList.toggle('active', linkHash === hash);
    });

    // Scroll to top
    window.scrollTo(0, 0);
  }

  window.addEventListener('hashchange', navigate);
  window.addEventListener('DOMContentLoaded', navigate);
})();

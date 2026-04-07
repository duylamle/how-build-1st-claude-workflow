(function() {
  var publicPages = ['home', 'login'];
  var loggedPages = ['dashboard', 'tasks', 'settings'];
  var allPages = publicPages.concat(loggedPages);

  function navigate() {
    var hash = location.hash.replace('#','') || 'home';
    if (allPages.indexOf(hash) === -1) hash = 'home';
    var isPublic = publicPages.indexOf(hash) !== -1;

    // Hide all pages, show target
    document.querySelectorAll('.page').forEach(function(p) {
      p.classList.remove('active');
    });
    var target = document.getElementById('page-' + hash);
    if (target) target.classList.add('active');

    // Toggle public vs logged headers
    var headerPublic = document.getElementById('header-public');
    var headerLogged = document.getElementById('header-logged');
    if (headerPublic) headerPublic.style.display = isPublic ? '' : 'none';
    if (headerLogged) headerLogged.style.display = isPublic ? 'none' : '';

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

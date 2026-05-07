/* Fahad Almansour Office — light/dark toggle + hamburger nav.
 * Ported from the static landing page (lines 566–587 of index.html).
 * The early-paint boot script in inc/enqueue.php sets data-theme before this
 * runs so reloads don't flash the wrong palette.
 */
(function () {
	'use strict';

	var html = document.documentElement;

	/* ── Theme toggle ── */
	var btn = document.getElementById('themeBtn');
	var ico = document.getElementById('themeIco');
	var txt = document.getElementById('themeTxt');

	var SUN  = '<path d="M12 1v2M12 21v2M4.22 4.22l1.42 1.42M18.36 18.36l1.42 1.42M1 12h2M21 12h2M4.22 19.78l1.42-1.42M18.36 5.64l1.42-1.42"/><circle cx="12" cy="12" r="5"/>';
	var MOON = '<path d="M21 12.79A9 9 0 1111.21 3a7 7 0 109.79 9.79z"/>';

	function paint(t) {
		if (ico) {
			ico.innerHTML = (t === 'dark') ? SUN : MOON;
			if (t === 'dark') {
				ico.setAttribute('fill', 'none');
				ico.setAttribute('stroke', 'currentColor');
				ico.setAttribute('stroke-width', '2');
				ico.setAttribute('stroke-linecap', 'round');
				ico.setAttribute('stroke-linejoin', 'round');
			} else {
				ico.setAttribute('fill', 'currentColor');
				ico.removeAttribute('stroke');
				ico.removeAttribute('stroke-width');
				ico.removeAttribute('stroke-linecap');
				ico.removeAttribute('stroke-linejoin');
			}
		}
		if (txt) {
			txt.textContent = (t === 'dark') ? 'Light' : 'Dark';
		}
	}

	function set(t) {
		html.setAttribute('data-theme', t);
		try { localStorage.setItem('theme', t); } catch (e) {}
		paint(t);
	}

	// Sync UI to whatever the boot script (or default) already chose.
	paint(html.getAttribute('data-theme') || 'light');

	if (btn) {
		btn.addEventListener('click', function () {
			set(html.getAttribute('data-theme') === 'dark' ? 'light' : 'dark');
		});
	}

	/* ── Hamburger ── */
	var ham = document.getElementById('hamburger');
	var nav = document.getElementById('navLinks');
	if (ham && nav) {
		ham.addEventListener('click', function () {
			nav.classList.toggle('open');
			var open = nav.classList.contains('open');
			ham.setAttribute('aria-expanded', open ? 'true' : 'false');
		});
		Array.prototype.forEach.call(nav.querySelectorAll('a'), function (a) {
			a.addEventListener('click', function () {
				nav.classList.remove('open');
				ham.setAttribute('aria-expanded', 'false');
			});
		});
	}
})();

// ─── CONFIG ───
const API = 'http://localhost:5000';  // change to your Render backend URL when deployed

// ─── MOBILE MENU ───
function toggleMenu() {
  document.getElementById('mobile-menu').classList.toggle('open');
}
document.addEventListener('click', function(e) {
  const menu = document.getElementById('mobile-menu');
  const ham  = document.getElementById('ham');
  if (menu && ham && !menu.contains(e.target) && !ham.contains(e.target)) {
    menu.classList.remove('open');
  }
});

// ─── ANIMATE BARS ON LOAD ───
window.addEventListener('load', () => {
  document.querySelectorAll('.skb-fill, .mi-fill, .progress-fill').forEach(el => {
    const w = el.style.width;
    el.style.width = '0';
    setTimeout(() => { el.style.width = w; }, 400);
  });
});
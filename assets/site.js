const menuButton = document.querySelector('.menu');
const nav = document.querySelector('.site-header nav');
const industryDropdown = document.querySelector('.nav-dropdown');
const industryButton = industryDropdown?.querySelector('button');

function setIndustryMenu(open) {
  industryDropdown?.classList.toggle('open', open);
  industryButton?.setAttribute('aria-expanded', String(open));
}

menuButton?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  menuButton.setAttribute('aria-expanded', String(open));
});

industryButton?.addEventListener('click', () => {
  setIndustryMenu(!industryDropdown.classList.contains('open'));
});

document.addEventListener('click', (event) => {
  if (!industryDropdown?.contains(event.target)) setIndustryMenu(false);
});

document.addEventListener('keydown', (event) => {
  if (event.key === 'Escape') setIndustryMenu(false);
});

const lightbox = document.querySelector('.image-lightbox');
const lightboxImage = lightbox?.querySelector('img');
const lightboxClose = lightbox?.querySelector('.lightbox-close');

document.querySelectorAll('.image-zoom').forEach((trigger) => {
  trigger.addEventListener('click', () => {
    lightboxImage.src = trigger.dataset.fullImage;
    lightboxImage.alt = trigger.dataset.imageAlt;
    lightbox.showModal();
  });
});

lightboxClose?.addEventListener('click', () => lightbox.close());
lightbox?.addEventListener('click', (event) => {
  if (event.target === lightbox) lightbox.close();
});

lightbox?.addEventListener('close', () => {
  lightboxImage.removeAttribute('src');
  lightboxImage.alt = '';
});

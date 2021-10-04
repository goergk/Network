document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.likes_container').addEventListener('click', () => likes_counter());
  });

function likes_counter() {
  if (document.querySelector('.heart_icon').alt === "like"){
    document.querySelector('.heart_icon').alt = "unlike"
    document.querySelector('.heart_icon').src = "\/static\/network/unlike.svg"
    document.querySelector('.likes_container').title = "Unlike"
  } else if (document.querySelector('.heart_icon').alt === "unlike"){
    document.querySelector('.heart_icon').alt = "like"
    document.querySelector('.heart_icon').src = "\/static\/network/like.svg"
    document.querySelector('.likes_container').title = "Like"
  }
}
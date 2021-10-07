document.addEventListener('DOMContentLoaded', function() {

    try{
      const elements = document.querySelectorAll('.likes_container');

      elements.forEach(element => {
        element.addEventListener('click', (e) => LikeOrUnlike_user(element)
        );
      });
    }catch(e){}

    try{
      document.querySelector('.follows_container').addEventListener('click', () => followOrUnfollow_user());
    }catch(e){}
  });

function LikeOrUnlike_user(element) {

  parentDiv = element.parentNode
  post_id = parentDiv.querySelector('.post_id').textContent;
  likes = element.querySelector('#likes_counter').textContent;
  currentUrl = window.location.href
  fetchURL = ''

  if (currentUrl.includes("/user")){
    // Handling likes on user profile page
    fetchURL = '/post/like/'+post_id

  } else{
    // Handling likes on index page
    fetchURL = 'post/like/'+post_id

  }

  fetch(fetchURL, {
    method: 'PUT'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Something went wrong');
    } else {
      if (element.querySelector('.heart_icon').alt === "like"){
        element.querySelector('.heart_icon').alt = "unlike"
        element.querySelector('.heart_icon').src = "\/static\/network/unlike.svg"
        element.title = "Unlike"

        likes = parseInt(likes) + 1
        element.querySelector('#likes_counter').textContent = likes

      } else if (element.querySelector('.heart_icon').alt === "unlike"){
        element.querySelector('.heart_icon').alt = "like"
        element.querySelector('.heart_icon').src = "\/static\/network/like.svg"
        element.title = "Like"

        likes = parseInt(likes) - 1
        element.querySelector('#likes_counter').textContent = likes
      }
    }
  })
}

function followOrUnfollow_user() {

  user = document.querySelector('#username').textContent;
  followers = document.querySelector('#followers_counter').textContent;

  fetch(user+'/follow', {
    method: 'PUT',
    credentials: 'include'
  })
  .then(response => {
    if (!response.ok) {
      throw new Error('Something went wrong');
    } else {
      if (document.querySelector('.follow_icon').alt === "follow"){
        document.querySelector('.follow_icon').alt = "unfollow"
        document.querySelector('.follow_icon').src = "\/static\/network/unfollow.svg"
        document.querySelector('.follow_text').textContent = "Unfollow"
        document.querySelector('.follow_text').style = "color: red"
    
        followers = parseInt(followers) + 1
        document.querySelector('#followers_counter').textContent = followers
    
      } else if (document.querySelector('.follow_icon').alt === "unfollow"){
        document.querySelector('.follow_icon').alt = "follow"
        document.querySelector('.follow_icon').src = "\/static\/network/follow.svg"
        document.querySelector('.follow_text').textContent = "Follow"
        document.querySelector('.follow_text').style = "color: green"
    
        followers = parseInt(followers) - 1
        document.querySelector('#followers_counter').textContent = followers

      }
    }
  })
}
document.addEventListener('DOMContentLoaded', function() {

    document.querySelector('.likes_container').addEventListener('click', () => likes_counter());
    try{
      document.querySelector('.follows_container').addEventListener('click', () => followOrUnfollow_user());
    }catch(e){}
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

function followOrUnfollow_user() {

  user = document.querySelector('#username').textContent;
  followers = document.querySelector('#followers_counter').textContent;

  fetch(user+'/follow', {
    method: 'PUT'
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